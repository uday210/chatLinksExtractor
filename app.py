import streamlit as st
import pandas as pd
from io import StringIO
from utils import extract_links, extract_names, parse_dates, group_by_month, categorize_link

st.set_page_config(page_title="Chat Link Extractor", layout="wide")
st.title("🔗 Chat Link Extractor")
st.markdown("Extract and organize links from chat histories (WhatsApp, Telegram, etc.)")

# Sidebar options
with st.sidebar:
    st.header("⚙️ Options")
    extract_names_toggle = st.checkbox("Include Names/Usernames", value=False)
    group_by_month_toggle = st.checkbox("Group by Month", value=True)
    deduplicate = st.checkbox("Remove Duplicates", value=True)
    
    # Link type filtering
    st.subheader("🔍 Link Filters")
    link_types = st.multiselect(
        "Select link types to extract:",
        ["Telegram", "Amazon", "YouTube", "GitHub", "Other"],
        default=["Telegram", "Amazon", "YouTube", "GitHub", "Other"],
        help="Choose which types of links to extract from your chat history"
    )

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input")
    input_method = st.radio("Select input method:", ["Paste Text", "Upload File"])
    
    if input_method == "Paste Text":
        text_input = st.text_area("Paste your chat history here:", height=300, placeholder="WhatsApp, Telegram, or any chat history in txt format...")
    else:
        uploaded_file = st.file_uploader("Upload .txt file", type='txt')
        if uploaded_file is not None:
            text_input = uploaded_file.read().decode('utf-8')
        else:
            text_input = ""

with col2:
    st.subheader("📊 Preview")
    if text_input:
        preview_lines = '\n'.join(text_input.split('\n')[:10])
        st.text_area("First 10 lines:", value=preview_lines, height=300, disabled=True)

# Process button
if st.button("🚀 Extract & Process", type="primary", use_container_width=True):
    if not text_input.strip():
        st.error("Please provide chat history text or upload a file!")
    else:
        with st.spinner("Processing..."):
            # Extract links with filtering
            links = extract_links(text_input, link_types)
            
            # Extract names if toggled
            names = extract_names(text_input) if extract_names_toggle else []
            
            # Parse dates and links together
            dated_links = parse_dates(text_input)
            
            # Filter dated_links based on selected link types
            filtered_dated_links = {}
            for date, urls in dated_links.items():
                filtered_urls = [url for url in urls if categorize_link(url) in link_types]
                if filtered_urls:
                    filtered_dated_links[date] = filtered_urls
            
            # Deduplicate if toggled
            if deduplicate:
                links = list(dict.fromkeys(links))  # Preserves order while deduping
                filtered_dated_links = {k: list(dict.fromkeys(v)) for k, v in filtered_dated_links.items()}
            
            # Group by month if toggled
            if group_by_month_toggle:
                grouped_data = group_by_month(filtered_dated_links, extract_names_toggle)
            else:
                grouped_data = []
                for date, urls in filtered_dated_links.items():
                    for url in urls:
                        grouped_data.append({"Date": date, "Link": url})
            
            # Display results
            st.success("✅ Processing complete!")
            
            # Show stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Links Found", len(links))
            with col2:
                st.metric("Unique Links", len(set(links)))
            with col3:
                st.metric("Names Found", len(set(names)) if names else 0)
            
            # Display table
            st.subheader("📋 Results")
            if isinstance(grouped_data, list) and grouped_data:
                df = pd.DataFrame(grouped_data)
                st.dataframe(df, use_container_width=True, height=400)
                
                # CSV Download
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv,
                    file_name="extracted_links.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("No links found in the provided text!")
            
            # Show extracted names if available
            if extract_names_toggle and names:
                st.subheader("👥 Names/Usernames Found")
                unique_names = sorted(list(set(names)))
                st.write(", ".join(unique_names))
                
                names_csv = pd.DataFrame({"Names": unique_names}).to_csv(index=False)
                st.download_button(
                    label="📥 Download Names as CSV",
                    data=names_csv,
                    file_name="extracted_names.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
        Made with ❤️ | Open source on <a href='https://github.com' target='_blank'>GitHub</a>
    </div>
""", unsafe_allow_html=True)
