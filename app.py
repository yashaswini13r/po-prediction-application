import json
import streamlit as st
from classifier import classify_po

st.set_page_config(page_title="PO Category Classifier", layout="centered")

st.title("📦 PO Category Classifier")

MAX_DESC_CHARS = 1500

st.caption(
    "Enter a clear, short PO description. Example: "
    "'Office cleaning services - March'."
)

with st.form("po_classify_form"):
    po_description = st.text_area(
        "PO Description",
        height=120,
        max_chars=MAX_DESC_CHARS,
        placeholder="e.g., DocuSign eSignature Enterprise Pro Subscription",
    )
    supplier = st.text_input(
        "Supplier (optional)",
        placeholder="e.g., DocuSign Inc",
    )
    classify_clicked = st.form_submit_button("Classify")

if classify_clicked:
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            supplier_value = supplier.strip() or "Not provided"
            try:
                result = classify_po(po_description.strip(), supplier_value)
            except Exception as exc:
                st.error("Classification failed. Please try again.")
                with st.expander("Error details"):
                    st.code(str(exc))
                st.stop()

            try:
                parsed = json.loads(result)
                l1 = parsed.get("L1", "Not sure")
                l2 = parsed.get("L2", "Not sure")
                l3 = parsed.get("L3", "Not sure")

                c1, c2, c3 = st.columns(3)
                c1.metric("L1", l1)
                c2.metric("L2", l2)
                c3.metric("L3", l3)

                st.json(parsed)
            except Exception:
                st.error("Invalid model response")
                st.text(result)

