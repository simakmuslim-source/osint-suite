"""
OSINT Suite – simple web UI (Streamlit)

Run:
    pip install streamlit
    streamlit run webapp.py
"""

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="OSINT Suite",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 OSINT Suite")
st.caption("Free local toolkit — Sherlock, phone, contacts, image hash, courts")

tab_user, tab_phone, tab_contacts, tab_image, tab_court, tab_report = st.tabs(
    ["Username", "Phone", "Contacts", "Image", "Courts", "Report"]
)

# ---------- Username ----------
with tab_user:
    st.subheader("Username search (Sherlock)")
    uname = st.text_input("Username", key="uname")
    if st.button("Search username", type="primary") and uname:
        with st.spinner("Running Sherlock..."):
            try:
                from core.username_search import search_username
                results = search_username(uname)
                found = [r for r in results if r.get("exists")]
                st.success(f"Found on {len(found)} sites")
                if found:
                    st.dataframe(
                        [{"site": r.get("site"), "url": r.get("url")} for r in found],
                        use_container_width=True,
                    )
                else:
                    st.info("No public profiles found (or Sherlock not installed).")
            except Exception as e:
                st.error(str(e))

# ---------- Phone ----------
with tab_phone:
    st.subheader("Phone lookup")
    phone = st.text_input("Phone (+7...)", key="phone")
    show_vk = st.checkbox("Show VK guidance", value=True)
    if st.button("Lookup phone", type="primary") and phone:
        from core.phone_lookup import lookup_phone
        from core.vk_osint import search_vk_by_phone, format_vk_result

        info = lookup_phone(phone)
        st.write(
            {
                "normalized": info.get("normalized"),
                "operator": info.get("operator"),
                "region": info.get("region"),
                "country": info.get("country"),
            }
        )
        if show_vk:
            st.code(format_vk_result(search_vk_by_phone(phone)))

# ---------- Contacts ----------
with tab_contacts:
    st.subheader("Extract contacts from URL")
    url = st.text_input("Page URL", key="url", placeholder="https://example.com")
    if st.button("Scrape contacts", type="primary") and url:
        with st.spinner("Scraping..."):
            from core.contact_scraper import scrape_contacts
            result = scrape_contacts(url)
            if result.get("error"):
                st.error(result["error"])
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Emails**")
                    st.write(result.get("emails") or "—")
                    st.markdown("**Phones**")
                    st.write(result.get("phones") or "—")
                with col2:
                    st.markdown("**Social**")
                    st.write(result.get("social") or "—")

# ---------- Image ----------
with tab_image:
    st.subheader("Local reverse image (perceptual hash)")
    uploaded = st.file_uploader("Query image", type=["jpg", "jpeg", "png", "webp"])
    db_folder = st.text_input("Database folder", value=".")
    threshold = st.slider("Max distance", 0, 20, 10)
    if st.button("Search similar", type="primary") and uploaded:
        tmp = Path("_tmp_query.jpg")
        tmp.write_bytes(uploaded.getvalue())
        try:
            from core.reverse_image import phash_search
            matches = phash_search(str(tmp), db_folder, threshold=threshold)
            if matches:
                st.dataframe(
                    [{"distance": d, "path": p} for p, d in matches],
                    use_container_width=True,
                )
            else:
                st.warning("No similar images found in the folder.")
        except Exception as e:
            st.error(str(e))
        finally:
            if tmp.exists():
                tmp.unlink()

# ---------- Courts ----------
with tab_court:
    st.subheader("Russian courts (guidance)")
    q = st.text_input("Name / case number", key="court_q")
    region = st.text_input("Region (optional)", key="court_region")
    year = st.number_input("Year (optional)", min_value=1990, max_value=2030, value=2024, step=1)
    if st.button("Court search", type="primary") and q:
        from core.court_search import search_cases, format_court_result
        data = search_cases(query=q, region=region or None, year=int(year))
        st.code(format_court_result(data))
        for u in data.get("suggested_urls") or []:
            st.markdown(f"- [{u}]({u})")

# ---------- Report ----------
with tab_report:
    st.subheader("Generate report")
    r_user = st.text_input("Username", key="r_user")
    r_phone = st.text_input("Phone", key="r_phone")
    r_url = st.text_input("Contacts URL", key="r_url")
    if st.button("Build report", type="primary"):
        username_data = phone_data = contacts_data = None

        if r_user:
            from core.username_search import search_username
            results = search_username(r_user)
            found = [r for r in results if r.get("exists")]
            username_data = {
                "query": r_user,
                "found": found,
                "total_checked": len(results),
            }

        if r_phone:
            from core.phone_lookup import lookup_phone
            from core.vk_osint import search_vk_by_phone
            phone_data = {
                "lookup": lookup_phone(r_phone),
                "vk": search_vk_by_phone(r_phone),
            }

        if r_url:
            from core.contact_scraper import scrape_contacts
            contacts_data = scrape_contacts(r_url)

        from core.report import build_report, to_markdown, save_report
        data = build_report(
            username_data=username_data,
            phone_data=phone_data,
            contacts_data=contacts_data,
        )
        md = to_markdown(data)
        save_report(data, md_path="report.md", json_path="report.json")

        st.markdown(md)
        st.download_button("Download report.md", md, file_name="report.md")
        st.success("Also saved as report.md / report.json in the working directory")

st.divider()
st.caption("osint-suite · free · local · MIT")
