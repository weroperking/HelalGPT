# HelalGPT  

HelalGPT is a specialized AI-powered web application designed to answer Islamic-related questions. It ensures logical reasoning and references from the Quran or authentic Hadith while maintaining a user-friendly interface.  

## Features  

- **Islamic Expertise:** Focused solely on Islamic inquiries, responding with well-reasoned and authentic answers.  
- **User-Friendly Interface:** Built using HTML, TailwindCSS, and JavaScript for a sleek and responsive design.  
- **Interactive Chat:** Seamless interaction with the AI model for real-time responses.  
- **API Integration:** Backend powered by Python (Flask) and Hugging Face transformers for advanced NLP.  
- **Error Handling:** Graceful fallbacks for invalid inputs or unrelated questions.  

## Technologies  

### Frontend:  
- **HTML & TailwindCSS**: Clean and modern styling.  
- **JavaScript**: Enables smooth interactivity with the API.  

### Backend:  
- **Python (Flask)**: Manages API endpoints and logic.  
- **Hugging Face Transformers**: Utilized for generating responses.  
- **Flask-CORS**: Ensures secure cross-origin requests.  

### Deployment:  
- Local deployment supported with Flask.  

## Installation  

1. Clone this repository:  
   ```bash  
        git clone https://github.com/weroperking/HelalGPT.git  
        cd HelalGPT  
        pip install -r requirements.txt
    ```
## Run the Flask server:
```python
python app.py  
``` 

- Open the application in your browser:
    Navigate to http://127.0.0.1:5000/.

## Usage
-Type a question in the input box, and HelalGPT will respond with an answer.
-If a question is unrelated to Islamic topics, the app will reply accordingly.

## Contribution
Contributions are welcome! If you have ideas for improving the project, feel free to fork this repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgments
-Hugging Face Community for providing robust NLP tools.
-Git-Hub for hosting this repository.
-Flask for its simplicity in building web applications.
-TailwindCSS for enabling responsive design effortlessly.