import sqlite3
import pandas as pd
import streamlit as st
from database import DATABASE

# Initialize DB
db = DATABASE()
db.create_table()

st.title("Product Record System")

## Display Products in a Table form

st.header("All Products")
products = db.fetch_products()

if not products:
    st.info("No products found.")
else:
    df = pd.DataFrame(products, columns=["Name", "Color", "Part Number", "Size (mm)"])

    # Table Header
    # Increased the width of the last two columns to avoid wrapping
    col1, col2, col3, col4, col5, col6 = st.columns([3, 3, 3, 2, 1.5, 1.5])
    col1.markdown("**Name**")
    col2.markdown("**Color**")
    col3.markdown("**Part Number**")
    col4.markdown("**Size (mm)**")
    col5.markdown("**Edit**")
    col6.markdown("**Delete**")

    # Table Rows
    for i, row in df.iterrows():
        name = row["Name"]
        color = row["Color"]
        part_number = row["Part Number"]
        size_mm = row["Size (mm)"]

        # If currently editing this row
        if st.session_state.get("edit_part_number") == part_number:
            e_col1, e_col2, e_col3, e_col4, e_col5, e_col6 = st.columns([3, 3, 3, 2, 1.5, 1.7])
            new_name = e_col1.text_input("Edit Name", value=name, key=f"edit_name_{part_number}")
            new_color = e_col2.text_input("Edit Color", value=color, key=f"edit_color_{part_number}")
            e_col3.markdown(f"`{part_number}`")
            new_size = e_col4.number_input(
                "Edit Size",
                value=int(size_mm),
                min_value=0,
                step=1,
                key=f"edit_size_{part_number}"
            )

            save = e_col5.button("save", key=f"save_{part_number}")
            cancel = e_col6.button("cancel", key=f"cancel_{part_number}")

            if save:
                db.modify_product(part_number, new_name, new_color, new_size)
                st.success("Product updated.")
                st.session_state["edit_part_number"] = None
                st.rerun()

            if cancel:
                st.session_state["edit_part_number"] = None
                st.rerun()

        else:
            # Normal (non-edit) row
            r_col1, r_col2, r_col3, r_col4, r_col5, r_col6 = st.columns([3, 3, 3, 2, 1.5, 1.7])
            r_col1.write(name)
            r_col2.write(color)
            r_col3.write(part_number)
            r_col4.write(size_mm)

            if r_col5.button("edit", key=f"edit_{part_number}"):
                st.session_state["edit_part_number"] = part_number
                st.rerun()

            if r_col6.button("delete", key=f"delete_{part_number}"):
                db.delete_product(part_number)
                st.warning(f"Deleted product {name} with Part #: {part_number}")
                st.rerun()


## Add a New Product

st.header("Add a New Product")
with st.form("add_product", clear_on_submit= True):
    name = st.text_input("Product Name")
    color = st.text_input("Color")
    part_number = st.text_input("Part Number (6–10 alphanumeric)")
    size = st.number_input("Size in mm", min_value=0, step=1)

    submitted = st.form_submit_button("Add Product")
    if submitted:
        if not (6 <= len(part_number) <= 10) or not part_number.isalnum():
            st.error("Part Number must be 6–10 alphanumeric characters.")
        else:
            try:
                db.insert_product(name, color, part_number, size)
                st.success("Product added successfully!")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("Part Number must be unique.")