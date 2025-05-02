Here’s a professional, portfolio-ready version of your README content, rewritten for clarity and polish, while still crediting the original source:

---

## 📊 Dataset Overview: PaySim – Mobile Money Fraud Simulation

**Dataset link**: [Kaggle – PaySim Financial Transactions Dataset](https://www.kaggle.com/datasets/ealaxi/paysim1)

---

### 🧠 Context

Access to real financial datasets is extremely limited due to privacy concerns, especially in the area of mobile money transactions—a rapidly growing domain in many parts of the world. This lack of data creates challenges for researchers working on fraud detection models.

To address this, the PaySim project simulates realistic mobile money transactions using a model trained on aggregated real-world data. This allows for experimentation with fraud detection techniques without compromising sensitive information.

---

### 📁 About the Dataset

PaySim generates synthetic transaction data based on actual mobile money logs from one month of financial activity provided by a multinational financial services company operating in over 14 countries across Africa.

The dataset shared on Kaggle is a scaled-down version (approximately one-quarter the size of the original), tailored for public use.

> **Note**: Fraudulent transactions in this dataset are cancelled, so columns like `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, and `newbalanceDest` should not be used directly for fraud detection tasks.

---

### 🧾 Data Structure

Each record includes key details of a transaction:

| Column | Description |
|--------|-------------|
| `step` | Time unit (1 step = 1 hour); total simulation time = 744 hours (30 days). |
| `type` | Transaction type: `CASH-IN`, `CASH-OUT`, `DEBIT`, `PAYMENT`, or `TRANSFER`. |
| `amount` | Transaction amount (in local currency). |
| `nameOrig` | ID of the transaction originator. |
| `oldbalanceOrg` | Balance of originator before the transaction. |
| `newbalanceOrig` | Balance of originator after the transaction. |
| `nameDest` | ID of the recipient. |
| `oldbalanceDest` | Recipient's balance before the transaction (missing for merchants). |
| `newbalanceDest` | Recipient's balance after the transaction (missing for merchants). |
| `isFraud` | Indicates whether the transaction was fraudulent. |
| `isFlaggedFraud` | Indicates whether the transaction was flagged (e.g., amount > 200,000). |

---

Sure! Here's a concise and professional section you can add to your README to explain the **types of transactions** in the PaySim dataset:

---

### 🔄 Transaction Types

The dataset includes **five types of mobile money transactions**, each representing common operations in real-world financial systems:

| Transaction Type | Description |
|------------------|-------------|
| **PAYMENT**      | Customer-to-business payments (e.g., bills, services). This is the most common transaction type and typically does not involve fraud. |
| **TRANSFER**     | Peer-to-peer transfers between individual accounts. Fraud often occurs here when malicious users attempt to move funds between compromised accounts. |
| **CASH-OUT**     | Withdrawing money from a mobile wallet, either at an agent location or ATM. Fraudsters often use this step to extract funds after transferring them. |
| **CASH-IN**      | Depositing money into a mobile wallet. It usually precedes a transfer or payment. This type is rarely linked to fraud. |
| **DEBIT**        | A less frequent operation; typically represents account fees or other deductions. This category is not associated with fraudulent behavior in this dataset. |

> In the simulation, **fraudulent activity is primarily seen in TRANSFER and CASH-OUT transactions**, reflecting a realistic fraud strategy where funds are first moved and then withdrawn.

---


### 🔬 Background & Research

The dataset is a result of multiple PaySim simulation runs using different random seeds, each representing a full month (744 steps) of mobile money activity. Each run generates around 24 million transaction records. 

More details about the methodology and experiments can be found in the author’s [PhD Thesis – Chapter 7](http://urn.kb.se/resolve?urn=urn:nbn:se:bth-12932).

---

### 🙌 Acknowledgements

This dataset is part of the research project **“Scalable resource-efficient systems for big data analytics”**, funded by the Knowledge Foundation (Grant No. 20140032) in Sweden.

---

### 📚 Citation

Please cite the original work when using this dataset:

> E. A. Lopez-Rojas, A. Elmir, and S. Axelsson. *“PaySim: A financial mobile money simulator for fraud detection.”* In: The 28th European Modeling and Simulation Symposium-EMSS, Larnaca, Cyprus. 2016.

---

Let me know if you’d like a Markdown version ready to drop into a `README.md` or if you want help tailoring this to a specific portfolio project!