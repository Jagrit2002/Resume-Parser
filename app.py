import streamlit as st
from parser_utils import ResumeParser
from save_utils import save_to_csv
import pandas as pd
import os

def main():
    st.title("📄 Resume Parser & Analyzer")

    parser = ResumeParser()

    # Initialize session state to avoid re-parsing on CSV download
    if "parsed_data" not in st.session_state:
        st.session_state.parsed_data = None
        st.session_state.full_text = None
        st.session_state.resume_uploaded = False

    if "last_uploaded_filename" not in st.session_state:
        st.session_state.last_uploaded_filename = None

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    if uploaded_file is not None:
        if uploaded_file.name != st.session_state.last_uploaded_filename:
            with st.spinner("Extracting text from resume..."):
                full_text = parser.extract_text_from_pdf(uploaded_file)

            with st.spinner("Parsing resume with LLM..."):
                parsed_data = parser.extract_with_llm(full_text)

            if not parsed_data:
                st.error("Failed to parse resume. Please try with a different resume.")
                return

            st.session_state.parsed_data = parsed_data
            st.session_state.full_text = full_text
            st.session_state.last_uploaded_filename = uploaded_file.name

            # Save to CSV
            save_to_csv(parsed_data)

    if st.session_state.parsed_data:
        parsed_data = st.session_state.parsed_data
        full_text = st.session_state.full_text

        # Load and download CSV only if it exists
        if os.path.exists("parsed_resume.csv"):
            df = pd.read_csv("parsed_resume.csv")
            st.download_button("⬇️ Download Resume Data as CSV", df.to_csv(index=False), file_name="parsed_resume.csv", mime="text/csv")

        # Display parsed sections nicely
        st.header("✅ Parsed Resume Data")

        if "Name" in parsed_data:
            st.markdown(f"👤 **Name:** {parsed_data['Name']}")
        if "Email" in parsed_data:
            st.markdown(f"📧 **Email:** {parsed_data['Email']}")
        if "Phone Number" in parsed_data:
            st.markdown(f"📞 **Phone Number:** {parsed_data['Phone Number']}")
        if "LinkedIn" in parsed_data and parsed_data["LinkedIn"]:
            st.markdown(f"[🔗 LinkedIn Profile]({parsed_data['LinkedIn']})")

        def display_section(title, content):
            st.subheader(f"📚 {title}")
            if isinstance(content, list):
                for i, item in enumerate(content):
                    st.markdown(f"**{title} {i+1}:**")
                    if isinstance(item, dict):
                        for k, v in item.items():
                            st.markdown(f"- **{k}:** {v}")
                    else:
                        st.markdown(f"- {item}")
                    st.write("")
            else:
                st.markdown(content)

        if "Education" in parsed_data:
            display_section("Education", parsed_data["Education"])
        if "Experience" in parsed_data:
            display_section("Experience", parsed_data["Experience"])
        if "Projects" in parsed_data:
            display_section("Projects", parsed_data["Projects"])
        if "Skills" in parsed_data:
            st.subheader("📚 Skills")
            if isinstance(parsed_data["Skills"], list):
                st.markdown("\n".join([f"- {skill}" for skill in parsed_data["Skills"]]))

        # Resume scoring
        st.header("🎯 Resume Skill Score")
        score, matched, missing = parser.calculate_score(parsed_data.get("Skills", []))
        st.markdown(f"**Score:** {score} / 100")
        st.markdown(f"**Matched Skills:** {', '.join(matched) if matched else 'None'}")
        st.markdown(f"**Missing Skills:** {', '.join(missing) if missing else 'None'}")

        # Ask questions about resume
        st.header("❓ Ask a Question about the Resume")
        question = st.text_input("Enter your question here:")
        if question:
            with st.spinner("Getting answer from LLM..."):
                answer = parser.ask_question(full_text, question)
            st.markdown(f"💡 **Answer:** {answer}")

if __name__ == "__main__":
    main()
