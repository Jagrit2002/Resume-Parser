# 📄 AI-Powered Resume Parser

A Streamlit-based web application that uses AI to parse and analyze resumes in PDF format. The application extracts key information like contact details, education, experience, projects, and skills from resumes, and provides a skill matching score based on a predefined skill set.

## 🚀 Features

- **PDF Resume Parsing**: Extract text from PDF resumes using PyMuPDF
- **AI-Powered Analysis**: Uses Ollama's LLM (Mistral model) to parse and structure resume data
- **Skill Matching**: Compares extracted skills against a predefined skill set
- **Interactive Q&A**: Ask questions about the resume content
- **CSV Export**: Save parsed data for further analysis
- **Responsive UI**: Clean and intuitive user interface

## 🛠️ Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)
- At least 4GB RAM (8GB recommended)
- NVIDIA GPU (optional, for better performance with Ollama)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Jagrit2002/Resume-Parser.git
cd resume-parser
```

### 2. Start the Application

Run the following command to start the application using Docker Compose:

```bash
docker compose up --build
```

This will:
1. Build the Docker images
2. Start the Streamlit application
3. Start the Ollama LLM server

### 3. Access the Application

Once the containers are up and running, open your web browser and navigate to:

```
http://localhost:8501
```

## 🖥️ Usage

1. Click on "Browse files" or drag and drop a PDF resume
2. Wait for the resume to be processed (this may take a moment)
3. View the parsed information including:
   - Contact details
   - Education history
   - Work experience
   - Projects
   - Skills
   - Skill matching score
4. Use the "Ask a Question" section to get more information from the resume
5. Download the parsed data as a CSV file using the download button

## 🏗️ Project Structure

- `app.py`: Main Streamlit application
- `parser_utils.py`: Contains the ResumeParser class for text extraction and LLM processing
- `save_utils.py`: Utilities for saving parsed data to CSV
- `Dockerfile`: Configuration for the Streamlit application container
- `docker-compose.yml`: Defines the multi-container setup (Streamlit + Ollama)
- `requirements.txt`: Python dependencies

## 🔧 Customization

### Skill Pool

You can customize the skill matching by modifying the `skill_pool` in the `ResumeParser` class in `parser_utils.py`.

### Model Selection

By default, the application uses the "mistral" model. You can change this by modifying the `model` attribute in the `ResumeParser` class.

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**: Ensure no other services are using ports 8501 (Streamlit) or 11434 (Ollama).
2. **GPU not detected**: The application will run on CPU if no compatible GPU is found.
3. **Memory issues**: If the application crashes, try increasing Docker's memory allocation.

### Logs

View container logs with:

```bash
docker compose logs -f
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Ollama](https://ollama.ai/) for the LLM backend
- [PyMuPDF](https://pypi.org/project/PyMuPDF/) for PDF text extraction
