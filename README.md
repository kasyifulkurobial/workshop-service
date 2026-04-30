# Odoo 17 Module: Workshop Service Management

[![Odoo Version](https://img.shields.io/badge/Odoo-17.0-purple.svg)](https://www.odoo.com/)
[![License](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0.html)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

## 📝 Overview

**Workshop Service** is a custom Odoo 17 module designed to optimize the end-to-end service center lifecycle. This module bridges technical field operations with commercial and logistics management, ensuring data accuracy between Service Orders, Sales, and Inventory.

## ✨ Key Technical Features

### 🔧 Core Management
*   **Centralized Service Records**: Comprehensive management of vehicle data, license/serial numbers, and technician assignments.
*   **Dynamic Service Lines**: Logical separation between service components (**Labor**) and physical components (**Spare Parts**).

### ⚙️ Automation & Business Logic
*   **Reactive Compute Engine**: Real-time calculation for Subtotal, Tax (11%), and Grand Total using Odoo's `api.depends`.
*   **Time-Tracking Logic**: Automated calculation of Service Duration Days to monitor technician KPIs.

### 🔄 Seamless Integration (Cross-Module)
*   **Sales Automation**: Automatic transformation of Service Lines into a Sale Order Quotation with a single click.
*   **Inventory Orchestration**: Automated generation of Stock Picking (Delivery Orders) featuring smart filters that only process physical products (Spare Parts), preventing manual data entry errors.

### 🛡️ Data Integrity & Validations
*   **Strict Operational Flow**: Status validation to ensure workflows adhere to standard operating procedures (Draft → Confirmed → In Progress → Done).
*   **Constraint Safeguards**: Prevention of duplicate Sales or Picking documents through relational ID reference checks.

## 🛠️ Tech Stack & Standards

*   **Framework**: Odoo 17 LGPL
*   **Backend**: Python 3.10+ following PEP8 standards
*   **Frontend**: XML, OWL (Odoo Web Library)
*   **Database**: PostgreSQL
*   **Design Pattern**: MVC (Model-View-Controller)

## 🚀 Quick Start

### Prerequisites
Ensure the following dependency modules are installed:
*   `base`
*   `sale_management`
*   `stock`

### Installation
1.  Clone the repository into your Odoo `custom_addons` directory:
    ```bash
    git clone [https://github.com/kasyifulkurobial/workshop-service.git](https://github.com/kasyifulkurobial/workshop-service.git)
    ```
2.  Update the *Addons Path* in your `odoo.conf` file.
3.  Restart the Odoo server and update the module list:
    ```bash
    ./odoo-bin -c odoo.conf -u workshop_service
    ```

## 🧪 User Acceptance Testing (UAT) Scenario

| Step | Action | Expected Result |
|---|---|---|
| 1 | Create New Service Order | Reference "New" generated, customer & vehicle data assigned. |
| 2 | Add Labor & Part Lines | Subtotal, Tax, and Grand Total calculated automatically. |
| 3 | Click 'Confirm' | Status changes to **Confirmed**, Action buttons appear. |
| 4 | Click 'Create Sale Order' | SO Quotation created with all 3 lines; Button is hidden. |
| 5 | Click 'Create Stock Picking' | Delivery Order created **exclusively** for Spare Part items. |

---

**Developed by:**
**Kasyiful Kurobi Alqorrosyai**
*Junior Odoo Developer*
[LinkedIn](https://www.linkedin.com/in/kasyiful-kurobi-alqorrosyai-2a59a0250) | [Email](mailto:kurobikasyiful14@gmail.com)
