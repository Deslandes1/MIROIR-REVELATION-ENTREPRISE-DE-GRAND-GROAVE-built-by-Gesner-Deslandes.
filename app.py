import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(
    page_title="Miroir Revelation Entreprise - Grand Goave",
    page_icon="🇭🇹",
    layout="wide"
)

# Supabase REST API configuration
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def supabase_insert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    response = requests.post(url, headers=headers, json=data)
    return response.status_code in (200, 201)

def supabase_select(table, filters=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    params = {}
    if filters:
        for k, v in filters.items():
            params[k] = f"eq.{v}"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return []

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.markdown("""
<style>
    .hero {
        background: linear-gradient(90deg, #00209f, #cf0921);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
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

def login_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="color: #00209f;">🇭🇹 MIROIR REVELATION</h1>
            <h2 style="color: #cf0921;">ENTREPRISE DE GRAND GOAVE</h2>
        </div>
        """, unsafe_allow_html=True)
        with st.form("login"):
            username = st.text_input("👤 Nom d'utilisateur")
            password = st.text_input("🔒 Mot de passe", type="password")
            if st.form_submit_button("🔐 Se connecter"):
                if username == "miroir" and password == "grandgoave2026":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")
        st.markdown("📞 (509) 4738-5663 | ✉️ deslandes78@gmail.com")

def main_dashboard():
    st.sidebar.image("https://flagcdn.com/ht.svg", width=80)
    st.sidebar.markdown("## Miroir Revelation")
    if st.sidebar.button("🚪 Déconnexion"):
        st.session_state.authenticated = False
        st.rerun()
    st.sidebar.markdown("---")
    st.sidebar.markdown("📞 (509) 4738-5663")
    st.sidebar.markdown("✉️ deslandes78@gmail.com")

    st.markdown("""
    <div class="hero">
        <h1>MIROIR REVELATION ENTREPRISE</h1>
        <p>Grand Goave – Gestion des ventes, cartes de coupe, transactions</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📦 Ventes", "💇 Coupe (250 HTG)", "💰 Moncash & Natcash", "📊 Rapports"])

    with tabs[0]:
        st.subheader("Enregistrer une vente")
        with st.form("sale"):
            article = st.text_input("Article")
            quantity = st.number_input("Quantité", 1, 1000, 1)
            price = st.number_input("Prix unitaire (HTG)", 0.0, 100000.0, 0.0)
            if st.form_submit_button("Enregistrer"):
                if article and quantity and price:
                    total = quantity * price
                    data = {
                        "article": article,
                        "quantity": quantity,
                        "price_haitian": price,
                        "total": total,
                        "sale_date": datetime.now().isoformat()
                    }
                    if supabase_insert("miroir_sales", data):
                        st.success("Vente enregistrée !")
                        st.rerun()
                    else:
                        st.error("Erreur d'enregistrement.")
        st.markdown("---")
        st.subheader("Ventes du jour")
        today = datetime.now().date().isoformat()
        sales = supabase_select("miroir_sales", {"sale_date": today}) if today else []
        if sales:
            df = pd.DataFrame(sales)
            st.dataframe(df[["article", "quantity", "price_haitian", "total"]])
            st.metric("Total", f"{df['total'].sum()} HTG")
        else:
            st.info("Aucune vente aujourd'hui.")

    with tabs[1]:
        st.subheader("Donner une carte de coupe (250 HTG)")
        with st.form("haircut"):
            barber = st.selectbox("Coiffeur", ["Fo", "Can"])
            if st.form_submit_button("Donner la carte"):
                data = {
                    "barber": barber,
                    "card_amount": 250,
                    "created_at": datetime.now().isoformat()
                }
                if supabase_insert("miroir_haircut_cards", data):
                    st.success(f"Carte donnée à {barber}")
                    st.rerun()
        st.markdown("---")
        st.subheader("Cartes du jour")
        today = datetime.now().date().isoformat()
        cards = supabase_select("miroir_haircut_cards", {"created_at": today}) if today else []
        if cards:
            df = pd.DataFrame(cards)
            st.dataframe(df[["barber", "card_amount"]])
            fo_count = len([c for c in cards if c["barber"]=="Fo"])
            can_count = len([c for c in cards if c["barber"]=="Can"])
            st.metric("Cartes Fo", fo_count)
            st.metric("Cartes Can", can_count)
        else:
            st.info("Aucune carte aujourd'hui.")

    with tabs[2]:
        st.subheader("Enregistrer une transaction")
        with st.form("transaction"):
            service = st.selectbox("Service", ["Moncash", "Natcash"])
            trans_type = st.selectbox("Type", ["deposit", "withdrawal"])
            amount = st.number_input("Montant (HTG)", 0.0, 10000000.0, 0.0)
            if st.form_submit_button("Enregistrer"):
                data = {
                    "service": service,
                    "type": trans_type,
                    "amount": amount,
                    "created_at": datetime.now().isoformat()
                }
                if supabase_insert("miroir_transactions", data):
                    st.success("Transaction enregistrée !")
                    st.rerun()
        st.markdown("---")
        st.subheader("Transactions du jour")
        today = datetime.now().date().isoformat()
        trans = supabase_select("miroir_transactions", {"created_at": today}) if today else []
        if trans:
            df = pd.DataFrame(trans)
            st.dataframe(df[["service", "type", "amount"]])
            deposits = sum(t["amount"] for t in trans if t["type"]=="deposit")
            withdrawals = sum(t["amount"] for t in trans if t["type"]=="withdrawal")
            st.metric("Dépôts", f"{deposits} HTG")
            st.metric("Retraits", f"{withdrawals} HTG")
        else:
            st.info("Aucune transaction aujourd'hui.")

    with tabs[3]:
        st.subheader("Télécharger les rapports")
        report = st.selectbox("Rapport", ["Ventes", "Cartes de coupe", "Transactions"])
        if st.button("Générer CSV"):
            if report == "Ventes":
                data = supabase_select("miroir_sales")
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button("Télécharger", csv, "ventes.csv", "text/csv")
            elif report == "Cartes de coupe":
                data = supabase_select("miroir_haircut_cards")
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button("Télécharger", csv, "cartes.csv", "text/csv")
            else:
                data = supabase_select("miroir_transactions")
                df = pd.DataFrame(data)
                csv = df.to_csv(index=False)
                st.download_button("Télécharger", csv, "transactions.csv", "text/csv")
            st.success("Rapport prêt !")

    st.markdown("""
    <div class="footer">
        <p>Construit par <strong>Gesner Deslandes</strong> pour GlobalInternet.py</p>
    </div>
    """, unsafe_allow_html=True)

if not st.session_state.authenticated:
    login_page()
else:
    main_dashboard()
