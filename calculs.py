# ============================================
# CALCULS SUCRERIE COSUMAR - VERSION COMPLÈTE
# Basé sur le document PDF SUTA OCT2014
# Module 1 : Paramètres de base (pages 15-29)
# Module 2 : Point de grainage & Cristallisation (pages 45-61)
# Module 3 : Diffusion & Soutirage (pages 127-231)
# Module 4 : Inversion du saccharose (pages 77, 244)
# Module 5 : Bilans massique & thermique (pages 207-219, 260-262)
# Module 6 : Qualité sucre blanc CEE (pages 265-271)
# ============================================

import math

# ============================================
# MODULE 1 : PARAMÈTRES DE BASE (pages 15-29)
# ============================================

def purete(pol, brix):
    """Page 24 : Pureté = (Pol / Brix) * 100"""
    if brix == 0:
        return 0
    return round((pol / brix) * 100, 2)

def salin(sucre, cendres):
    """Page 27 : Salin = Sucre / Cendres"""
    if cendres == 0:
        return 0
    return round(sucre / cendres, 2)

def rapport_organique_cendres(ns_organique, cendres):
    """Page 28 : O/C = Non sucre organique / Cendres"""
    if cendres == 0:
        return 0
    return round(ns_organique / cendres, 2)

def baume_to_brix(baume, temp_c):
    """Page 18 : Conversion Baumé -> Brix"""
    baume_corr = baume + 0.05 * (temp_c - 15)
    brix = (baume_corr - 2.3) * 2
    return round(brix, 2)

def densite_jus_brix(brix, temp_c=20):
    """Page 18 : Densité à partir du Brix"""
    if temp_c >= 160:
        facteur_temp = 1
    else:
        facteur_temp = 1 - (0.036 * (temp_c - 20) / (160 - temp_c))
    densite = (1 + (brix * (brix + 200) / 54000)) * facteur_temp
    return round(densite, 4)

def cendres_conductivite(conductivite_us):
    """Page 27 : Cendres % = Conductivité x 0.0018"""
    return round(conductivite_us * 0.0018, 3)

# ============================================
# MODULE 2 : POINT DE GRAINAGE & CRISTALLISATION (pages 45-61)
# ============================================

def solubilite_vavrinecz(temp_c):
    """Page 52-53 : Brix de saturation à température donnée (eau pure)
    Formule de Vavrinecz (1962)
    """
    t = temp_c
    brix = (64.447 + 0.0822 * t + 0.0016169 * t**2 - 0.00001558 * t**3 - 0.0000000463 * t**4)
    return round(brix, 2)

def se_saturation_vavrinecz(temp_c):
    """Calcule S/E à saturation (sucre/eau) à partir du Brix"""
    brix = solubilite_vavrinecz(temp_c)
    if brix >= 100:
        return 999
    se = brix / (100 - brix)
    return round(se, 3)

def coeff_sursaturation(se_actuel, se_saturation):
    """Page 46 : K = (S/E actuel) / (S/E saturation)
    K < 1 : sous-saturée, K = 1 : saturée, K > 1 : sursaturée
    """
    if se_saturation == 0:
        return 0
    return round(se_actuel / se_saturation, 3)

def zone_cristallisation(K):
    """Page 50 : Détermine la zone de cristallisation"""
    if K < 1.0:
        return "Sous-saturée (pas de cristallisation)"
    elif K < 1.2:
        return "Métastable (cristallisation sur graines)"
    elif K < 1.3:
        return "Intermédiaire (nucléation hétérogène)"
    else:
        return "Labile (nucléation spontanée - risque de grainage fin)"

def point_grainage_recommande(temp_c, purete=88):
    """Calcule le point de grainage recommandé (sursaturation K = 1.1 à 1.2)"""
    se_sat = se_saturation_vavrinecz(temp_c)
    K_cible = 1.15
    se_cible = K_cible * se_sat
    brix_cible = (100 * se_cible) / (1 + se_cible)
    return {
        "temp_c": temp_c,
        "brix_cible": round(brix_cible, 1),
        "se_cible": round(se_cible, 3),
        "k_cible": K_cible,
        "zone": "Métastable (recommandé pour grainage)"
    }

def brix_saturation_kaganov(temp_c):
    """Page 49 : Formule de Kaganov"""
    T = temp_c + 273
    log_brix = 46.71038 + (1944.26 / T) + 17.17974 * math.log10(T)
    brix = 10 ** log_brix
    return round(brix, 2)

# ============================================
# MODULE 3 : DIFFUSION & SOUTIRAGE (pages 127-231)
# ============================================

def soutirage_gts(pol_cossettes, pertes_pulpe, sucre_jus_gl):
    """Page 220 : Formule GTS France - Soutirage volume (L/100kg cossettes)"""
    pertes_indet = 0.13
    if sucre_jus_gl == 0:
        return 0
    return round(100 * (pol_cossettes - (pertes_pulpe + pertes_indet)) / sucre_jus_gl, 2)

def soutirage_iris(pol_cossettes, pertes_pulpe, sucre_jus_gl):
    """Page 221 : Formule IRIS"""
    if sucre_jus_gl == 0:
        return 0
    return round(100 * (pol_cossettes - (pertes_pulpe * 1.3)) / sucre_jus_gl, 2)

def facteur_temperature_siline(temp_c):
    """Page 228 : Facteur Θ pour formule de Siline"""
    return round((2.35 * temp_c) - 81.0273, 2)

def duree_diffusion_rt(nb_compartiments, vitesse_tr_h):
    """Page 229 : Durée de diffusion pour RT (minutes)"""
    if vitesse_tr_h == 0:
        return 0
    return round((nb_compartiments * 60) / vitesse_tr_h, 1)

def constante_siline(gamma, L, theta, t):
    """Page 228 : Constante de diffusion K = gamma / (L * theta * t)"""
    if L * theta * t == 0:
        return 0
    return f"{gamma / (L * theta * t):.2e}"

# ============================================
# MODULE 4 : INVERSION DU SACCHAROSE (pages 77, 244)
# ============================================

def perte_inversion_anderson(pH, temps_min, temp_c):
    """Page 77/244 : % sucre hydrolysé par inversion
    log S = 18.68 - pH + log t - 5580/T
    """
    T_kelvin = temp_c + 273
    if T_kelvin <= 0:
        return 0
    log_S = 18.68 - pH + math.log10(temps_min) - (5580 / T_kelvin)
    S = 10 ** log_S
    return round(S, 3)

# ============================================
# MODULE 5 : BILANS MASSIQUE & THERMIQUE (pages 207-219, 260-262)
# ============================================

def marc_cossettes(pol_cossettes):
    """Page 212 : M cf = 0.117 x Pol + 2.555"""
    return round(0.117 * pol_cossettes + 2.555, 3)

def marc_pulpe_pressee(ms_pulpe, pol_pulpe):
    """Page 212 : M pp = MS - 0.895 x Pol - 0.29"""
    return round(ms_pulpe - 0.895 * pol_pulpe - 0.29, 3)

def quantite_pulpe_pressee(q_cossettes, m_cf, m_pp):
    """Page 212 : Q pp = Q cf x M cf / M pp"""
    if m_pp == 0:
        return 0
    return round(q_cossettes * m_cf / m_pp, 2)

def eau_evaporee_sechage(q_pp, ms_pp, ms_paillettes):
    """Page 260 : Eau évaporée au séchage"""
    if ms_paillettes == 0:
        return 0
    return round(q_pp * (ms_pp / 100) * (1 - ms_pp / ms_paillettes), 2)

def rendement_sechage(fuel_consomme, eau_evaporee, pci_fuel=9600):
    """Page 261 : Rendement du four (%)"""
    if eau_evaporee == 0:
        return 0
    chaleur_theorique = eau_evaporee * 624.8
    chaleur_fournie = fuel_consomme * pci_fuel
    return round(100 * chaleur_theorique / chaleur_fournie, 2)

# ============================================
# MODULE 6 : QUALITÉ SUCRE BLANC CEE (pages 265-271)
# ============================================

def points_europeens_aspect(type_couleur):
    """Page 266 : Points aspect = type_couleur x 2 (type de 0 à 6)"""
    return type_couleur * 2

def points_europeens_coloration(icu_units):
    """Page 267 : Points coloration = ICUMSA / 7.5"""
    return round(icu_units / 7.5, 1)

def points_europeens_cendres(pct_cendres):
    """Page 270 : Points cendres = pct_cendres / 0.0018"""
    if 0.0018 == 0:
        return 0
    return round(pct_cendres / 0.0018, 1)

def total_points_europeens(aspect, coloration, cendres):
    """Page 271 : Somme des 3 critères"""
    return aspect + coloration + cendres

def qualite_cee_from_points(total_points):
    """Page 271 : Détermine la catégorie de qualité"""
    if total_points <= 8:
        return "N°1 (Extra fin)"
    elif total_points <= 13:
        return "N°2 (Standard)"
    elif total_points <= 18:
        return "N°3 (Courant)"
    else:
        return "Hors norme"

# ============================================
# MODULE 7 : TABLES DE DONNÉES
# ============================================

# Table des masses volumiques (page 273-274)
MASSES_VOLUMIQUES = {
    "betterave_fraiche": 590,
    "cossettes_fraiches": 360,
    "pulpe_fraiche": 600,
    "pulpe_seche_paillettes": 220,
    "pellets": 580,
    "sucre_blanc": 810,
    "melasse": 1400,
    "fuel_lourd": 948,
}

def masse_volumique(produit):
    """Retourne la masse volumique en kg/m3"""
    return MASSES_VOLUMIQUES.get(produit, "Produit non trouvé")

# Table des pH caractéristiques (page 30-31)
PH_PRODUITS = {
    "jus_diffusion": (5.8, 6.5, 6.2),
    "jus_pre_chaulage": (11.2, 11.3, 11.25),
    "jus_1ere_co2": (10.8, 11.2, 11.0),
    "jus_2eme_co2": (9.0, 9.2, 9.1),
    "sirop_sortie_evap": (8.8, 9.2, 9.0),
    "melasse": (8.2, 8.5, 8.35),
    "sucre_blanc": (7.0, 7.3, 7.15),
}

def ph_typique(produit):
    """Retourne (min, max, moyenne) du pH"""
    return PH_PRODUITS.get(produit, "Produit non trouvé")
