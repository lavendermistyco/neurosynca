# NeuroSynca

![Neuro (1)](https://github.com/user-attachments/assets/fb55ad4a-e280-4b2e-aadd-b38d621a02f5)

NeuroSynca is a mental health chatbot designed specifically for Black and Latino communities. Utilizing the OpenAI API LLM, NeuroSynca aims to provide accessible mental health support to those who may not have the means to afford traditional healthcare services.

## Features

- **Mental Health Support**: Provides mental health assistance through a chatbot interface.
- **Community Focused**: Tailored for Black and Latino communities.
- **Affordable Access**: Aims to bridge the gap for those who cannot afford traditional healthcare.
- 
![Capture24](https://github.com/user-attachments/assets/1f1d04ba-f25f-4fca-bde0-c0f61b559360)
![Capture33](https://github.com/user-attachments/assets/c2fa2702-126b-42f7-b1ca-61c2f16e1443)
![54343](https://github.com/user-attachments/assets/fbb7e9a4-e742-4e77-8209-c5639696dd71)
![54353](https://github.com/user-attachments/assets/1933e62c-dfa6-4ff8-a714-bf1d5813acb0)



## Getting Started

### Prerequisites

- Python 3.x
- OpenAI API Key
- Google Places API Key

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/lavendermistyco/neurosynca.git
    ```
2. Navigate to the project directory:
    ```bash
    cd neurosynca
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
### Additional Setup

Before running the application, ensure the following files are present in the project directory:

- `chat_history.db`
- `users.xlsx`

### Environment Variables

Set your environment variables for the Google Places API and OpenAI API by adding the following lines to your `.bashrc` file:

```bash
export GOOGLE_API_KEY=your_google_api_key
export OPENAI_API_KEY=your_openai_api_key
```

After adding these lines, reload your `.bashrc` file:

```bash
source ~/.bashrc
```

### Running the Application

To run the application, execute the following command:
```bash
flask run
```


## Deployment

The application is hosted on Hostinger and connected to GitHub via CloudPanel for continuous deployment.

## Contributing

We welcome contributions! To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.


## Contact

For more information, please contact us at [info@uaxashaktun.tech](mailto:info@uaxashaktun.tech).
