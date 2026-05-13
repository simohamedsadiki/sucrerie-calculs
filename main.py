# ============================================
# APPLICATION SUCRERIE COSUMAR - INTERFACE MODERNE
# Tous les calculs - Version Complète
# ============================================

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.core.window import Window

import calculs

# Configuration de la fenêtre (taille téléphone)
Window.size = (360, 640)
Window.clearcolor = (0.95, 0.95, 0.95, 1)


class EcranParametres(ScrollView):
    """Module 1 : Paramètres de base (Brix, Pureté, Salin)"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=2, spacing=10, padding=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(Label(text='[b]PARAMÈTRES DE BASE[/b]', markup=True, size_hint_y=None, height=40))
        layout.add_widget(Label(text='', size_hint_y=None, height=40))
        
        # Pureté
        layout.add_widget(Label(text='Polarisation (%):'))
        self.pol_input = TextInput(text='15.5', multiline=False, input_filter='float')
        layout.add_widget(self.pol_input)
        
        layout.add_widget(Label(text='Brix:'))
        self.brix_input = TextInput(text='17.6', multiline=False, input_filter='float')
        layout.add_widget(self.brix_input)
        
        layout.add_widget(Label(text='[b]Purete calculée:[/b]', markup=True))
        self.purete_label = Label(text='-')
        layout.add_widget(self.purete_label)
        
        # Salin
        layout.add_widget(Label(text='Sucre (%):'))
        self.sucre_input = TextInput(text='15.0', multiline=False, input_filter='float')
        layout.add_widget(self.sucre_input)
        
        layout.add_widget(Label(text='Cendres (%):'))
        self.cendres_input = TextInput(text='0.5', multiline=False, input_filter='float')
        layout.add_widget(self.cendres_input)
        
        layout.add_widget(Label(text='[b]Salin calculé:[/b]', markup=True))
        self.salin_label = Label(text='-')
        layout.add_widget(self.salin_label)
        
        # Baumé → Brix
        layout.add_widget(Label(text='Baumé:'))
        self.baume_input = TextInput(text='15.0', multiline=False, input_filter='float')
        layout.add_widget(self.baume_input)
        
        layout.add_widget(Label(text='Température (°C):'))
        self.temp_baume_input = TextInput(text='20', multiline=False, input_filter='float')
        layout.add_widget(self.temp_baume_input)
        
        btn_baume = Button(text='Convertir Baumé → Brix', size_hint_y=None, height=40)
        btn_baume.bind(on_press=self.convertir_baume)
        layout.add_widget(btn_baume)
        
        self.baume_resultat = Label(text='Brix: -')
        layout.add_widget(self.baume_resultat)
        
        # Bouton global
        btn_calc = Button(text='CALCULER TOUS LES PARAMÈTRES', size_hint_y=None, height=50, background_color=(0.2, 0.6, 0.2, 1))
        btn_calc.bind(on_press=self.calculer_tout)
        layout.add_widget(btn_calc)
        
        self.add_widget(layout)
    
    def calculer_tout(self, instance):
        try:
            pol = float(self.pol_input.text)
            brix = float(self.brix_input.text)
            p = calculs.purete(pol, brix)
            self.purete_label.text = f'{p}%'
        except:
            self.purete_label.text = 'Erreur'
        
        try:
            sucre = float(self.sucre_input.text)
            cendres = float(self.cendres_input.text)
            s = calculs.salin(sucre, cendres)
            self.salin_label.text = f'{s}'
        except:
            self.salin_label.text = 'Erreur'
    
    def convertir_baume(self, instance):
        try:
            baume = float(self.baume_input.text)
            temp = float(self.temp_baume_input.text)
            b = calculs.baume_to_brix(baume, temp)
            self.baume_resultat.text = f'Brix: {b}'
        except:
            self.baume_resultat.text = 'Erreur'


class EcranPointGrainage(ScrollView):
    """Module 2 : Point de grainage & Cristallisation"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=2, spacing=10, padding=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(Label(text='[b]POINT DE GRAINAGE[/b]', markup=True, size_hint_y=None, height=40))
        layout.add_widget(Label(text='', size_hint_y=None, height=40))
        
        layout.add_widget(Label(text='Température (°C):'))
        self.temp_input = TextInput(text='70', multiline=False, input_filter='float')
        layout.add_widget(self.temp_input)
        
        layout.add_widget(Label(text='Brix actuel:'))
        self.brix_actuel_input = TextInput(text='75', multiline=False, input_filter='float')
        layout.add_widget(self.brix_actuel_input)
        
        btn_solubilite = Button(text='Calculer solubilité', size_hint_y=None, height=40)
        btn_solubilite.bind(on_press=self.calculer_solubilite)
        layout.add_widget(btn_solubilite)
        
        self.solubilite_label = Label(text='Brix saturation: -')
        layout.add_widget(self.solubilite_label)
        
        btn_sursat = Button(text='Calculer sursaturation', size_hint_y=None, height=40)
        btn_sursat.bind(on_press=self.calculer_sursat)
        layout.add_widget(btn_sursat)
        
        self.sursat_label = Label(text='K: -')
        layout.add_widget(self.sursat_label)
        
        btn_grainage = Button(text='Point de grainage recommandé', size_hint_y=None, height=40, background_color=(0.2, 0.5, 0.8, 1))
        btn_grainage.bind(on_press=self.calculer_grainage)
        layout.add_widget(btn_grainage)
        
        self.grainage_label = Label(text='Résultat: -', markup=True)
        layout.add_widget(self.grainage_label)
        
        self.add_widget(layout)
    
    def calculer_solubilite(self, instance):
        try:
            temp = float(self.temp_input.text)
            brix_sat = calculs.solubilite_vavrinecz(temp)
            self.solubilite_label.text = f'Brix saturation: {brix_sat}'
        except:
            self.solubilite_label.text = 'Erreur'
    
    def calculer_sursat(self, instance):
        try:
            temp = float(self.temp_input.text)
            brix_actuel = float(self.brix_actuel_input.text)
            brix_sat = calculs.solubilite_vavrinecz(temp)
            se_actuel = brix_actuel / (100 - brix_actuel)
            se_sat = brix_sat / (100 - brix_sat)
            K = calculs.coeff_sursaturation(se_actuel, se_sat)
            zone = calculs.zone_cristallisation(K)
            self.sursat_label.text = f'K = {K}\n{zone}'
        except:
            self.sursat_label.text = 'Erreur'
    
    def calculer_grainage(self, instance):
        try:
            temp = float(self.temp_input.text)
            resultat = calculs.point_grainage_recommande(temp)
            self.grainage_label.text = f'Brix cible: {resultat["brix_cible"]}\nS/E cible: {resultat["se_cible"]}\n{resultat["zone"]}'
        except:
            self.grainage_label.text = 'Erreur'


class EcranSoutirage(ScrollView):
    """Module 3 : Diffusion & Soutirage"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=2, spacing=10, padding=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(Label(text='[b]SOUTIRAGE - FORMULE GTS[/b]', markup=True, size_hint_y=None, height=40))
        layout.add_widget(Label(text='', size_hint_y=None, height=40))
        
        layout.add_widget(Label(text='Pol cossettes (%):'))
        self.pol_input = TextInput(text='18.0', multiline=False, input_filter='float')
        layout.add_widget(self.pol_input)
        
        layout.add_widget(Label(text='Pertes pulpe (% Bett):'))
        self.pertes_input = TextInput(text='0.18', multiline=False, input_filter='float')
        layout.add_widget(self.pertes_input)
        
        layout.add_widget(Label(text='Sucre jus (g%mL):'))
        self.sucre_input = TextInput(text='15.5', multiline=False, input_filter='float')
        layout.add_widget(self.sucre_input)
        
        btn_calc = Button(text='CALCULER SOUTIRAGE', size_hint_y=None, height=50, background_color=(0.2, 0.6, 0.2, 1))
        btn_calc.bind(on_press=self.calculer)
        layout.add_widget(btn_calc)
        
        self.resultat_label = Label(text='Résultat: -', markup=True)
        layout.add_widget(self.resultat_label)
        
        self.add_widget(layout)
    
    def calculer(self, instance):
        try:
            pol = float(self.pol_input.text)
            pertes = float(self.pertes_input.text)
            sucre = float(self.sucre_input.text)
            sv = calculs.soutirage_gts(pol, pertes, sucre)
            self.resultat_label.text = f'Soutirage = {sv} L/100kg'
        except:
            self.resultat_label.text = 'Erreur de saisie'


class EcranInversion(ScrollView):
    """Module 4 : Inversion du saccharose"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=2, spacing=10, padding=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(Label(text='[b]INVERSION DU SACCHAROSE[/b]', markup=True, size_hint_y=None, height=40))
        layout.add_widget(Label(text='', size_hint_y=None, height=40))
        
        layout.add_widget(Label(text='pH:'))
        self.ph_input = TextInput(text='5.8', multiline=False, input_filter='float')
        layout.add_widget(self.ph_input)
        
        layout.add_widget(Label(text='Temps (minutes):'))
        self.temps_input = TextInput(text='80', multiline=False, input_filter='int')
        layout.add_widget(self.temps_input)
        
        layout.add_widget(Label(text='Température (°C):'))
        self.temp_input = TextInput(text='72', multiline=False, input_filter='float')
        layout.add_widget(self.temp_input)
        
        btn_calc = Button(text='CALCULER PERTE', size_hint_y=None, height=50, background_color=(0.8, 0.4, 0.1, 1))
        btn_calc.bind(on_press=self.calculer)
        layout.add_widget(btn_calc)
        
        self.resultat_label = Label(text='Résultat: -', markup=True)
        layout.add_widget(self.resultat_label)
        
        self.add_widget(layout)
    
    def calculer(self, instance):
        try:
            pH = float(self.ph_input.text)
            t = float(self.temps_input.text)
            temp = float(self.temp_input.text)
            perte = calculs.perte_inversion_anderson(pH, t, temp)
            self.resultat_label.text = f'Perte = {perte}% sucre hydrolysé'
        except:
            self.resultat_label.text = 'Erreur de saisie'


class EcranQualite(ScrollView):
    """Module 6 : Qualité sucre blanc CEE"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=2, spacing=10, padding=20, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(Label(text='[b]QUALITÉ SUCRE CEE[/b]', markup=True, size_hint_y=None, height=40))
        layout.add_widget(Label(text='', size_hint_y=None, height=40))
        
        layout.add_widget(Label(text='Type couleur (0-6):'))
        self.aspect_input = TextInput(text='4', multiline=False, input_filter='int')
        layout.add_widget(self.aspect_input)
        
        layout.add_widget(Label(text='ICUMSA:'))
        self.color_input = TextInput(text='30', multiline=False, input_filter='float')
        layout.add_widget(self.color_input)
        
        layout.add_widget(Label(text='Cendres (%):'))
        self.cendres_input = TextInput(text='0.011', multiline=False, input_filter='float')
        layout.add_widget(self.cendres_input)
        
        btn_calc = Button(text='CALCULER POINTS CEE', size_hint_y=None, height=50, background_color=(0.2, 0.4, 0.6, 1))
        btn_calc.bind(on_press=self.calculer)
        layout.add_widget(btn_calc)
        
        self.resultat_label = Label(text='Résultat: -', markup=True)
        layout.add_widget(self.resultat_label)
        
        self.add_widget(layout)
    
    def calculer(self, instance):
        try:
            aspect = int(self.aspect_input.text)
            icu = float(self.color_input.text)
            cendres = float(self.cendres_input.text)
            
            pts_aspect = calculs.points_europeens_aspect(aspect)
            pts_couleur = calculs.points_europeens_coloration(icu)
            pts_cendres = calculs.points_europeens_cendres(cendres)
            total = calculs.total_points_europeens(pts_aspect, pts_couleur, pts_cendres)
            qualite = calculs.qualite_cee_from_points(total)
            
            self.resultat_label.text = f'Points: {total}\nQualité: {qualite}\n(Aspect:{pts_aspect} Col:{pts_couleur} Cen:{pts_cendres})'
        except:
            self.resultat_label.text = 'Erreur de saisie'


class AppSucrerieComplete(App):
    """Application principale avec onglets"""
    def build(self):
        panel = TabbedPanel()
        panel.default_tab_text = "Accueil"
        panel.tab_width = Window.width / 6
        
        # Module 1: Paramètres de base
        tab1 = TabbedPanelHeader(text="📊 Base")
        tab1.content = EcranParametres()
        panel.add_widget(tab1)
        
        # Module 2: Point de grainage
        tab2 = TabbedPanelHeader(text="🔬 Grainage")
        tab2.content = EcranPointGrainage()
        panel.add_widget(tab2)
        
        # Module 3: Soutirage
        tab3 = TabbedPanelHeader(text="🧪 Soutirage")
        tab3.content = EcranSoutirage()
        panel.add_widget(tab3)
        
        # Module 4: Inversion
        tab4 = TabbedPanelHeader(text="⚠️ Inversion")
        tab4.content = EcranInversion()
        panel.add_widget(tab4)
        
        # Module 5: Qualité
        tab5 = TabbedPanelHeader(text="⭐ Qualité")
        tab5.content = EcranQualite()
        panel.add_widget(tab5)
        
        return panel


if __name__ == '__main__':
    AppSucrerieComplete().run()
