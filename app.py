import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import os

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Miroir Revelation Entreprise - Grand Goave",
    page_icon="🇭🇹",
    layout="wide"
)

# ========== SUPABASE SETUP ==========
# Use nested secrets as defined in .streamlit/secrets.toml
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ========== SESSION STATE ==========
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f0f4ff 0%, #e8f0fe 100%);
    }
    .hero {
        background: linear-gradient(90deg, #00209f, #cf0921);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00209f, #cf0921);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        background-color: #f1f1f1;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ========== LOGIN PAGE ==========
def login_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #00209f;">🇭🇹 MIROIR REVELATION</h1>
            <h2 style="color: #cf0921;">ENTREPRISE DE GRAND GOAVE</h2>
            <p>Gestion des ventes, cartes de coupe, transactions Moncash/Natcash</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login"):
            username = st.text_input("👤 Nom d'utilisateur")
            password = st.text_input("🔒 Mot de passe", type="password")
            if st.form_submit_button("🔐 Se connecter", use_container_width=True):
                if username == "miroir" and password == "grandgoave2026":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Identifiants incorrects. Contactez Gesner Deslandes.")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <p>📞 (509) 4738-5663 | ✉️ deslandes78@gmail.com</p>
            <p>Construit par <strong>Gesner Deslandes</strong> pour GlobalInternet.py</p>
        </div>
        """, unsafe_allow_html=True)

# ========== MAIN DASHBOARD ==========
def main_dashboard():
    # Sidebar
    st.sidebar.image("https://flagcdn.com/ht.svg", width=80)
    st.sidebar.markdown("## 🇭🇹 Miroir Revelation")
    st.sidebar.markdown("**Grand Goave**")
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Contact:**")
    st.sidebar.markdown("📞 (509) 4738-5663")
    st.sidebar.markdown("✉️ deslandes78@gmail.com")
    st.sidebar.markdown("---")
    st.sidebar.markdown("© 2026 GlobalInternet.py")
    
    # Main header
    st.markdown("""
    <div class="hero">
        <h1>MIROIR REVELATION ENTREPRISE</h1>
        <p>Grand Goave – Gestion complète de vos activités</p>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["📦 Ventes", "💇 Coupe (Cartes 250 HTG)", "💰 Moncash & Natcash", "📊 Rapports"])
    
    # ---------- TAB 0: SALES ----------
    with tabs[0]:
        st.subheader("Enregistrer une vente")
        with st.form("sale_form"):
            col1, col2 = st.columns(2)
            with col1:
                article = st.text_input("Article vendu")
                quantity = st.number_input("Quantité", min_value=1, step=1)
            with col2:
                price = st.number_input("Prix unitaire (HTG)", min_value=0.0, step=10.0)
                total = quantity * price
                st.metric("Total", f"{total} HTG")
            if st.form_submit_button("💾 Enregistrer la vente"):
                if article and quantity and price:
                    supabase.table("miroir_sales").insert({
                        "article": article,
                        "quantity": quantity,
                        "price_haitian": price,
                        "total": total,
                        "sale_date": datetime.now().isoformat()
                    }).execute()
                    st.success("Vente enregistrée !")
                    st.rerun()
                else:
                    st.error("Veuillez remplir tous les champs.")
        
        st.markdown("---")
        st.subheader("Ventes du jour")
        today = datetime.now().date()
        sales = supabase.table("miroir_sales").select("*").gte("sale_date", today.isoformat()).execute().data
        if sales:
            df = pd.DataFrame(sales)
            st.dataframe(df[["article", "quantity", "price_haitian", "total"]])
            st.metric("Total des ventes aujourd'hui", f"{df['total'].sum()} HTG")
        else:
            st.info("Aucune vente aujourd'hui.")
    
    # ---------- TAB 1: HAIRCUT CARDS ----------
    with tabs[1]:
        st.subheader("Donner une carte de coupe (250 HTG)")
        with st.form("haircut_form"):
            barber = st.selectbox("Choisir le coiffeur", ["Fo", "Can"])
            if st.form_submit_button("💈 Donner la carte"):
                supabase.table("miroir_haircut_cards").insert({
                    "barber": barber,
                    "card_amount": 250,
                    "created_at": datetime.now().isoformat()
                }).execute()
                st.success(f"Carte de 250 HTG donnée à {barber}")
                st.rerun()
        
        st.markdown("---")
        st.subheader("Cartes données aujourd'hui")
        today_str = datetime.now().date().isoformat()
        cards = supabase.table("miroir_haircut_cards").select("*").gte("created_at", today_str).execute().data
        if cards:
            df_cards = pd.DataFrame(cards)
            st.dataframe(df_cards[["barber", "card_amount"]])
            st.metric("Total cartes Fo", len([c for c in cards if c["barber"]=="Fo"]))
            st.metric("Total cartes Can", len([c for c in cards if c["barber"]=="Can"]))
        else:
            st.info("Aucune carte donnée aujourd'hui.")
    
    # ---------- TAB 2: MONCASH / NATCASH ----------
    with tabs[2]:
        st.subheader("Enregistrer une transaction")
        with st.form("transaction_form"):
            service = st.selectbox("Service", ["Moncash", "Natcash"])
            trans_type = st.selectbox("Type", ["deposit", "withdrawal"])
            amount = st.number_input("Montant (HTG)", min_value=0.0, step=100.0)
            if st.form_submit_button("💵 Enregistrer"):
                supabase.table("miroir_transactions").insert({
                    "service": service,
                    "type": trans_type,
                    "amount": amount,
                    "created_at": datetime.now().isoformat()
                }).execute()
                st.success(f"{service} - {trans_type} de {amount} HTG enregistré.")
                st.rerun()
        
        st.markdown("---")
        st.subheader("Transactions du jour")
        today_trans = supabase.table("miroir_transactions").select("*").gte("created_at", datetime.now().date().isoformat()).execute().data
        if today_trans:
            df_trans = pd.DataFrame(today_trans)
            st.dataframe(df_trans[["service", "type", "amount"]])
            deposits = df_trans[df_trans["type"]=="deposit"]["amount"].sum()
            withdrawals = df_trans[df_trans["type"]=="withdrawal"]["amount"].sum()
            st.metric("Total dépôts", f"{deposits} HTG")
            st.metric("Total retraits", f"{withdrawals} HTG")
        else:
            st.info("Aucune transaction aujourd'hui.")
    
    # ---------- TAB 3: REPORTS ----------
    with tabs[3]:
        st.subheader("Télécharger les rapports")
        report_type = st.selectbox("Type de rapport", ["Ventes", "Cartes de coupe", "Transactions"])
        if st.button("📥 Générer et télécharger CSV"):
            if report_type == "Ventes":
                data = supabase.table("miroir_sales").select("*").execute().data
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button("Télécharger CSV", csv, "ventes.csv", "text/csv")
            elif report_type == "Cartes de coupe":
                data = supabase.table("miroir_haircut_cards").select("*").execute().data
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button("Télécharger CSV", csv, "cartes_coupe.csv", "text/csv")
            else:
                data = supabase.table("miroir_transactions").select("*").execute().data
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button("Télécharger CSV", csv, "transactions.csv", "text/csv")
            st.success("Rapport prêt !")
    
    st.markdown("""
    <div class="footer">
        <p>Construit par <strong>Gesner Deslandes</strong> pour GlobalInternet.py</p>
        <p>📞 (509) 4738-5663 | ✉️ deslandes78@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

# ========== ROUTING ==========
if not st.session_state.authenticated:
    login_page()
else:
    main_dashboard()
