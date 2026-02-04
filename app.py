import json
import streamlit as st
from classifier import MODEL, classify_po

st.set_page_config(page_title="PO Category Classifier", layout="centered")

st.title("📦 PO Category Classifier")

MAX_DESC_CHARS = 1500

if "po_description" not in st.session_state:
    st.session_state.po_description = ""
if "supplier" not in st.session_state:
    st.session_state.supplier = ""

with st.sidebar:
    st.subheader("Model")
    st.code(MODEL)
    debug = st.toggle("Show debug info", value=False)

st.caption(
    "Enter a clear, short PO description. Examples: "
    "'DocuSign eSignature subscription' or 'Office cleaning services - March'."
)

po_description = st.text_area(
    "PO Description",
    height=120,
    key="po_description",
    max_chars=MAX_DESC_CHARS,
    placeholder="e.g., DocuSign eSignature Enterprise Pro Subscription",
)
supplier = st.text_input(
    "Supplier (optional)",
    key="supplier",
    placeholder="e.g., DocuSign Inc",
)

col_a, col_b = st.columns(2)
with col_a:
    classify_clicked = st.button("Classify", type="primary")
with col_b:
    reset_clicked = st.button("Reset")

if reset_clicked:
    st.session_state.po_description = ""
    st.session_state.supplier = ""
    st.rerun()

if len(po_description.strip()) >= MAX_DESC_CHARS:
    st.warning(
        f"Description is at the {MAX_DESC_CHARS} character limit. "
        "Consider shortening for better results."
    )


@st.cache_data(show_spinner=False)
def cached_classify(description: str, supplier_value: str):
    return classify_po(description, supplier_value)


if classify_clicked:
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            supplier_value = supplier.strip() or "Not provided"
            try:
                result = cached_classify(po_description.strip(), supplier_value)
            except Exception as exc:
                st.error("Classification failed. Please try again.")
                with st.expander("Error details"):
                    st.code(str(exc))
                st.stop()

            if debug:
                st.write("Input supplier used:", supplier_value)

            try:
                parsed = json.loads(result)
                l1 = parsed.get("L1", "Not sure")
                l2 = parsed.get("L2", "Not sure")
                l3 = parsed.get("L3", "Not sure")

                c1, c2, c3 = st.columns(3)
                c1.metric("L1", l1)
                c2.metric("L2", l2)
                c3.metric("L3", l3)

                with st.expander("Raw JSON"):
                    st.json(parsed)

                st.download_button(
                    "Download JSON",
                    data=json.dumps(parsed, indent=2),
                    file_name="po_classification.json",
                    mime="application/json",
                )
            except Exception:
                st.error("Invalid model response")
                st.text(result)
