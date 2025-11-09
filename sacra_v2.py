#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SACRA V2 - Mit vollständiger I-Ging Integration

Erweitert das SACRA-System um die komplette I-Ging Datenbank:
- Hexagramm-Namen und Bedeutungen
- Urteile und Bilder
- Wandlungslinien
- Tiefere semantische Interpretation
"""

import sys
import argparse
from datetime import datetime, timedelta
from typing import Optional

# Import SACRA-Module
try:
    from sacra_system import SacraSystem
    from sacra_iching_integration import WandlungErweitert, IChingDatabase
except ImportError as e:
    print(f"FEHLER beim Import: {e}")
    print("\nBitte stelle sicher, dass alle Module vorhanden sind:")
    print("  - sacra_system.py")
    print("  - sacra_iching_integration.py")
    print("  - pi_pulse_integrated.py")
    print("  - wandlung.py")
    print("  - maya_kalender.py")
    print("  - hex64_database_full.json")
    sys.exit(1)


class SacraV2(SacraSystem):
    """
    Erweiterte SACRA-Version mit vollständiger I-Ging Integration.
    """
    
    def __init__(self):
        """Initialisiert SACRA V2 mit I-Ging Datenbank."""
        super().__init__()
        
        # Ersetze Wandlung durch erweiterte Version
        try:
            self.wandlung = WandlungErweitert()
            self.iching_db = self.wandlung.iching_db
            self.iching_verfuegbar = True
            print("✓ I-Ging Datenbank erfolgreich geladen")
        except FileNotFoundError as e:
            print(f"⚠ Warnung: I-Ging Datenbank nicht gefunden")
            print(f"   {e}")
            print("   Verwende Basis-Wandlung ohne erweiterte Texte")
            self.iching_verfuegbar = False
    
    def berechne_sacra_punkt_v2(self, datum: Optional[datetime] = None) -> dict:
        """
        Berechnet erweiterten SACRA-Zustandspunkt mit I-Ging Informationen.
        
        Args:
            datum: Datum für Berechnung (Standard: jetzt)
            
        Returns:
            Dict mit allen SACRA-Daten inkl. I-Ging Details
        """
        # Basis SACRA-Berechnung
        sacra_punkt = self.berechne_sacra_punkt(datum)
        
        # Erweitere mit I-Ging Informationen wenn verfügbar
        if self.iching_verfuegbar:
            hex_vollstaendig = self.wandlung.berechne_hexagramm_vollstaendig(datum)
            interpretation = self.wandlung.interpretiere_moment(datum)
            
            # Integriere I-Ging Daten
            sacra_punkt['wandlung_erweitert'] = {
                'name': hex_vollstaendig['name'],
                'urteil': hex_vollstaendig['urteil'],
                'struktur': hex_vollstaendig['struktur'],
                'aktive_linie': hex_vollstaendig['aktive_linie'],
                'gewandelt': hex_vollstaendig['wandlung'],
                'beziehungen': hex_vollstaendig['beziehungen']
            }
            
            sacra_punkt['interpretation'] = interpretation
            
            # Erweitere Qualitätsbewertung
            sacra_punkt['qualitaet']['iching_qualitaet'] = self._bewerte_iching_qualitaet(
                hex_vollstaendig, interpretation
            )
        
        return sacra_punkt
    
    def _bewerte_iching_qualitaet(self, hex_data: dict, interp: dict) -> dict:
        """
        Bewertet die I-Ging Qualität eines Moments.
        
        Args:
            hex_data: Hexagramm-Daten
            interp: Interpretation
            
        Returns:
            Dict mit I-Ging spezifischer Qualitätsbewertung
        """
        urteil = hex_data['urteil'].lower()
        
        # Positiv-Indikatoren
        positiv_woerter = ['gelingen', 'heil', 'fördernd', 'erfolg', 'glück']
        negativ_woerter = ['unheil', 'gefahr', 'unheil', 'schaden', 'makel']
        
        positiv_score = sum(2 for wort in positiv_woerter if wort in urteil)
        negativ_score = sum(2 for wort in negativ_woerter if wort in urteil)
        
        # Balance-Bewertung
        balance = hex_data['struktur']['balance']
        balance_score = (6 - balance) * 2  # Besser je ausgeglichener
        
        # Gesamt-Score (0-100)
        gesamt = min(100, max(0, (positiv_score * 10 + balance_score * 5 - negativ_score * 10)))
        
        # Qualitätsstufe
        if gesamt >= 70:
            stufe = "GÜNSTIG"
        elif gesamt >= 50:
            stufe = "NEUTRAL"
        elif gesamt >= 30:
            stufe = "HERAUSFORDERND"
        else:
            stufe = "SCHWIERIG"
        
        return {
            'score': gesamt,
            'stufe': stufe,
            'zeitqualitaet': interp['zeitqualitaet'],
            'energie_qualitaet': interp['energie_qualitaet']
        }
    
    def zeige_sacra_v2_zustand(self, sacra_punkt: dict, detailliert: bool = True):
        """
        Zeigt erweiterten SACRA-Zustand mit I-Ging Informationen.
        
        Args:
            sacra_punkt: SACRA V2 Zustandspunkt
            detailliert: Vollständige oder kompakte Ausgabe
        """
        print(f"\n{'═'*80}")
        print(f"{'SACRA V2 - MIT I-GING INTEGRATION':^80}")
        print(f"{'═'*80}")
        
        datum = sacra_punkt['datum']
        print(f"\n⏰ ZEITPUNKT: {datum.strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"🔐 SIGNATUR: {sacra_punkt['sacra_signatur']}")
        
        # Qualität
        qual = sacra_punkt['qualitaet']
        print(f"\n{'─'*80}")
        print(f"✨ SACRA-QUALITÄT: {qual['qualitaet']} ({qual['score']:.1f}/100)")
        print(f"   {qual['beschreibung']}")
        
        # I-Ging Qualität wenn verfügbar
        if 'iching_qualitaet' in qual:
            iching_qual = qual['iching_qualitaet']
            print(f"\n🔯 I-GING QUALITÄT: {iching_qual['stufe']} ({iching_qual['score']:.1f}/100)")
            print(f"   Zeitqualität: {iching_qual['zeitqualitaet']}")
            print(f"   Energie: {iching_qual['energie_qualitaet']}")
        
        if detailliert and 'wandlung_erweitert' in sacra_punkt:
            wdl_ext = sacra_punkt['wandlung_erweitert']
            
            # Hexagramm mit Namen
            print(f"\n{'─'*80}")
            print(f"🔄 I-GING HEXAGRAMM")
            print(f"{'─'*80}")
            print(f"Nr. {sacra_punkt['wandlung']['hexagramm_nummer']}: {wdl_ext['name']}")
            print(f"  Oben:  {sacra_punkt['wandlung']['trigramm_oben']['symbol']} "
                  f"{sacra_punkt['wandlung']['trigramm_oben']['name']}")
            print(f"  Unten: {sacra_punkt['wandlung']['trigramm_unten']['symbol']} "
                  f"{sacra_punkt['wandlung']['trigramm_unten']['name']}")
            
            # Struktur
            struktur = wdl_ext['struktur']
            print(f"\n   Struktur: {struktur['yang_linien']} Yang, {struktur['yin_linien']} Yin")
            balance_viz = "●" * (6 - struktur['balance']) + "○" * struktur['balance']
            print(f"   Balance:  {balance_viz}")
            
            # Essenz aus Urteil
            urteil_lines = wdl_ext['urteil'].split('\n')
            essenz = urteil_lines[0].strip() if urteil_lines else ""
            if essenz:
                print(f"\n   📜 Essenz: {essenz}")
            
            # Aktive Wandlungslinie
            if wdl_ext['aktive_linie']['daten']:
                linie = wdl_ext['aktive_linie']
                print(f"\n   ⚡ Aktive Linie {linie['position']}: {linie['daten']['title']}")
                linie_text = linie['daten']['text'].replace('\n', ' ').strip()
                if len(linie_text) > 100:
                    linie_text = linie_text[:97] + "..."
                print(f"      {linie_text}")
            
            # Wandlung
            if wdl_ext['gewandelt']:
                gewandelt = wdl_ext['gewandelt']
                print(f"\n   🔄 Wandlung zu: Nr. {gewandelt['gewandeltes_hexagramm_nr']} - "
                      f"{gewandelt['gewandeltes_hexagramm_name']}")
            
            # Beziehungen (kompakt)
            bez = wdl_ext['beziehungen']
            print(f"\n   🔗 Beziehungen:")
            print(f"      Kern: {bez['kern']['name']}")
        
        # Interpretation
        if 'interpretation' in sacra_punkt and detailliert:
            interp = sacra_punkt['interpretation']
            print(f"\n{'─'*80}")
            print(f"💡 INTERPRETATION & EMPFEHLUNG")
            print(f"{'─'*80}")
            print(f"   {interp['handlungs_empfehlung']}")
            
            trans = interp['transformation']
            print(f"\n   🔄 Transformation:")
            print(f"      {trans['aktuell']} → {trans['wandlung_zu']}")
        
        # Pi-Pulse, Maya und Energie wie im Original
        if detailliert:
            pp = sacra_punkt['pi_pulse']
            print(f"\n{'─'*80}")
            print(f"🌀 PI-PULSE")
            print(f"{'─'*80}")
            print(f"   Ziffer: {pp['ziffer']}")
            print(f"   Fibonacci-Radius: {pp['fibonacci_radius']:,}")
            print(f"   Welle: {pp['welle_nummer']}/20, Position: {pp['position_in_welle']}/13")
            
            maya = sacra_punkt['maya']
            print(f"\n{'─'*80}")
            print(f"📅 MAYA-KALENDER")
            print(f"{'─'*80}")
            print(f"   Tzolkin: {maya['tzolkin']['nummer']} {maya['tzolkin']['tag']}")
            print(f"   Haab: {maya['haab']['tag']} {maya['haab']['monat']}")
            print(f"   Venus: {maya['venus']['phase']}")
            
            ef = sacra_punkt['energie_feld']
            print(f"\n{'─'*80}")
            print(f"⚡ ENERGIE-FELD")
            print(f"{'─'*80}")
            print(f"   Intensität: {ef['intensitaet']}")
            print(f"   Modulierte Energie: {ef['modulierte_energie']:.1f}/100")
        
        print(f"\n{'═'*80}\n")
    
    def finde_guenstige_momente_v2(self, start: datetime, ende: datetime,
                                   min_sacra_qualitaet: float = 70.0,
                                   min_iching_qualitaet: float = 60.0,
                                   max_ergebnisse: int = 10) -> list:
        """
        Findet günstige Momente basierend auf SACRA und I-Ging Qualität.
        
        Args:
            start: Start-Datum
            ende: End-Datum
            min_sacra_qualitaet: Minimale SACRA-Qualität (0-100)
            min_iching_qualitaet: Minimale I-Ging-Qualität (0-100)
            max_ergebnisse: Maximale Anzahl Ergebnisse
            
        Returns:
            Liste von günstigen SACRA-Momenten
        """
        tage = (ende - start).days
        kandidaten = []
        
        print(f"Analysiere {tage} Tage...")
        
        for i in range(tage + 1):
            if i % 10 == 0:
                print(f"  {i}/{tage} Tage analysiert...", end='\r')
            
            aktuelles_datum = start + timedelta(days=i)
            sacra_punkt = self.berechne_sacra_punkt_v2(aktuelles_datum)
            
            sacra_qual = sacra_punkt['qualitaet']['score']
            
            # Prüfe I-Ging Qualität wenn verfügbar
            iching_qual = 0
            if 'iching_qualitaet' in sacra_punkt['qualitaet']:
                iching_qual = sacra_punkt['qualitaet']['iching_qualitaet']['score']
            
            # Beide Kriterien müssen erfüllt sein
            if sacra_qual >= min_sacra_qualitaet and iching_qual >= min_iching_qualitaet:
                kandidaten.append({
                    'sacra_punkt': sacra_punkt,
                    'gesamt_score': (sacra_qual + iching_qual) / 2
                })
        
        print(f"  {tage}/{tage} Tage analysiert... Fertig!")
        
        # Sortiere nach Gesamt-Score
        kandidaten.sort(key=lambda x: x['gesamt_score'], reverse=True)
        
        return [k['sacra_punkt'] for k in kandidaten[:max_ergebnisse]]


def main():
    """Hauptfunktion mit Demonstrationen."""
    parser = argparse.ArgumentParser(
        description="SACRA V2 - Mit vollständiger I-Ging Integration"
    )
    parser.add_argument('-d', '--datum', type=str, metavar='YYYY-MM-DD',
                       help='Analysiere spezifisches Datum')
    parser.add_argument('-o', '--optimal', action='store_true',
                       help='Finde optimale Momente im nächsten Monat')
    parser.add_argument('--tage', type=int, default=30,
                       help='Anzahl Tage für Suche (Standard: 30)')
    parser.add_argument('-k', '--kompakt', action='store_true',
                       help='Kompakte Ausgabe')
    
    args = parser.parse_args()
    
    # Initialisiere SACRA V2
    print("\n" + "="*80)
    print("SACRA V2 - INITIALIZATION")
    print("="*80 + "\n")
    
    sacra = SacraV2()
    
    if not sacra.iching_verfuegbar:
        print("\n⚠  I-Ging Datenbank nicht verfügbar - Verwende Basis-Version")
        print("   Für volle Funktionalität: hex64_database_full.json bereitstellen\n")
    
    # Parse Datum
    datum = None
    if args.datum:
        try:
            datum = datetime.strptime(args.datum, '%Y-%m-%d')
        except ValueError:
            print(f"FEHLER: Ungültiges Datumsformat. Verwende YYYY-MM-DD")
            sys.exit(1)
    
    if args.optimal:
        # Finde optimale Momente
        print("\n" + "="*80)
        print("SUCHE NACH OPTIMALEN MOMENTEN")
        print("="*80 + "\n")
        
        heute = datetime.now()
        ende = heute + timedelta(days=args.tage)
        
        optimale = sacra.finde_guenstige_momente_v2(
            heute, ende,
            min_sacra_qualitaet=70.0,
            min_iching_qualitaet=60.0,
            max_ergebnisse=5
        )
        
        if optimale:
            print(f"\n✨ {len(optimale)} optimale Momente gefunden:\n")
            for idx, moment in enumerate(optimale, 1):
                datum_str = moment['datum'].strftime('%d.%m.%Y %A')
                sacra_qual = moment['qualitaet']['score']
                signatur = moment['sacra_signatur']
                
                hex_name = "N/A"
                if 'wandlung_erweitert' in moment:
                    hex_name = moment['wandlung_erweitert']['name']
                
                print(f"{idx}. {datum_str}")
                print(f"   Signatur: {signatur}")
                print(f"   SACRA-Qualität: {sacra_qual:.1f}/100")
                print(f"   Hexagramm: {hex_name}")
                
                if 'iching_qualitaet' in moment['qualitaet']:
                    iching_qual = moment['qualitaet']['iching_qualitaet']
                    print(f"   I-Ging: {iching_qual['stufe']} ({iching_qual['score']:.1f}/100)")
                print()
        else:
            print("\n❌ Keine optimalen Momente gefunden.")
    
    else:
        # Standard: Zeige aktuellen oder spezifischen Moment
        if datum is None:
            datum = datetime.now()
        
        print("\n" + "="*80)
        print("SACRA V2 - MOMENT-ANALYSE")
        print("="*80)
        
        sacra_punkt = sacra.berechne_sacra_punkt_v2(datum)
        sacra.zeige_sacra_v2_zustand(sacra_punkt, detailliert=not args.kompakt)


if __name__ == "__main__":
    main()
