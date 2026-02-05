# ⚖️ Wanna Call? - Framework de Auditoría OSINT y Automatización

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Propósito-Educativo-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Licencia-MIT-orange?style=for-the-badge" />
</p>

> **"Verificación de Identidad y Automatización de Servicios."**

---

## 🇪🇸 ESPAÑOL (Documentación Principal)

**Wanna Call?** es una prueba de concepto (PoC) diseñada para demostrar las capacidades de la automatización moderna con Python en los campos de la **Inteligencia de Fuentes Abiertas (OSINT)** y la **Automatización Web**. Esta herramienta sirve como recurso educativo para investigadores de ciberseguridad, desarrolladores y auditores de privacidad que deseen comprender cómo se indexa la información pública y cómo los servicios web gestionan las interacciones automatizadas.

### ⚠️ AVISO LEGAL Y PROPÓSITO EDUCATIVO

**LEA ATENTAMENTE ANTES DE UTILIZAR ESTE SOFTWARE.**

Este software ha sido desarrollado y se distribuye **ÚNICAMENTE CON FINES EDUCATIVOS**. Su intención es ayudar a los usuarios a auditar su **propia** huella digital y entender la importancia de la privacidad y los límites de velocidad (rate-limiting) en los servicios web.

*   **Consentimiento:** Usted debe realizar escaneos o pruebas de automatización únicamente sobre datos, números o servicios que **sean de su propiedad** o para los cuales tenga **permiso explícito**.
*   **Responsabilidad:** Los desarrolladores y colaboradores de este repositorio **no asumen ninguna responsabilidad** por el mal uso o los daños causados por este software.
*   **Cumplimiento Normativo:** Los usuarios son responsables de cumplir con todas las leyes locales, estatales y federales aplicables (incluyendo el RGPD en Europa) en materia de privacidad de datos y comunicaciones electrónicas.

**Al descargar o utilizar este software, usted acepta estos términos.**

---

### 🔍 Características Clave

Este framework integra múltiples módulos para demostrar la recopilación y gestión de datos:

#### 1. 🕵️‍♂️ Motor Avanzado OSINT (Verificación de Identidad)
Herramientas diseñadas para auditar la exposición pública de información personal (Teléfonos, Nombres de Usuario).
*   **Análisis de Huella Digital:** Referencia cruzada de números de teléfono en fuentes públicas.
*   **Fuentes Oficiales:** Indexación de boletines oficiales del estado (BOE, Boletines Provinciales).
*   **Grafo Social:** Detección de cuentas asociadas en plataformas como Spotify, Pinterest o LinkedIn.
*   **Detección de Fugas:** Comprobación de posible exposición de datos en brechas públicas (Auditoría de Privacidad).
*   **Minería de Contexto:** Extracción de metadatos relevantes de fragmentos de búsqueda pública.

#### 2. 🤖 Módulo de Automatización de Servicios (Pruebas de Estrés)
Ejemplos de automatización de navegadores "headless" (sin interfaz gráfica) utilizando `Selenium` y `Undetected-Chromedriver`.
*   **Interacción con Formularios:** Rerenado y verificación automatizada de formularios web.
*   **Gestión de Captchas:** Investigación sobre la detección automatizada de desafíos de seguridad.
*   **Ejecución Multihilo:** Demostración de capacidades de procesamiento paralelo para tareas de alto rendimiento.
*   **Gestión de Proxies:** Implementación de lógica de rotación para mantener la estabilidad de la conexión.

#### 3. 🛠️ Arquitectura Profesional
*   **Interfaz Visual:** GUI moderna construida con `CustomTkinter`.
*   **Sistema de Auto-Actualización:** Mecanismo binario que se actualiza a sí mismo integrado con GitHub Releases.
*   **Sistema de Compilación Robusto:** Tubería de compilación automatizada para generar ejecutables independientes (.exe).

---

### 🚀 Instalación y Uso

#### Requisitos Previos
*   Python 3.11 o superior
*   Google Chrome (para módulos de automatización)

#### Inicio Rápido (Código Fuente)

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/kevinkgp92/wannacallbot.git
    cd wannacallbot
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Si faltan módulos específicos, ejecute `tools/install_deps.py`)*

3.  **Ejecutar la aplicación:**
    ```bash
    python gui.py
    ```

#### Para Desarrolladores / Compilación
Para generar un ejecutable independiente (.exe):
1.  Asegúrese de tener activo el entorno de Python correcto.
2.  Ejecute el script de compilación (o use el modo "God Mode"):
    ```bash
    python build_pro.py
    ```
3.  El ejecutable aparecerá en la carpeta `dist/`.

---

<br>
<br>

---

## 🇺🇸 ENGLISH (Secondary Documentation)

**Wanna Call?** is a research proof-of-concept (PoC) designed to demonstrate the capabilities of modern Python automation in the fields of **Open Source Intelligence (OSINT)** and **Web Automation**. It serves as an educational tool for cybersecurity researchers, developers, and privacy auditors to understand how public data is indexed and how web services handle automated interactions.

### ⚠️ LEGAL DISCLAIMER & EDUCATIONAL PURPOSE

**PLEASE READ CAREFULLY BEFORE USING THIS SOFTWARE.**

This software is developed and distributed for **EDUCATIONAL PURPOSES ONLY**. It is intended to help users audit their **own** digital footprint and understand the importance of privacy and rate-limiting on web services.

*   **Consent:** You must only perform scans or automation tests on data/numbers/services that **you own** or have **explicit permission** to audit.
*   **Liability:** The developers and contributors of this repository admit **no liability** and are not responsible for any misuse or damage caused by this software.
*   **Compliance:** Users are responsible for complying with all applicable local, state, and federal laws (including GDPR in Europe) regarding data privacy and electronic communications.

**By downloading or using this software, you agree to these terms.**

---

### 🔍 Key Features

This framework integrates multiple modules to demonstrate automated data gathering and interaction:

#### 1. 🕵️‍♂️ Advanced OSINT Engine (Identity Verification)
Tools designed to audit the public exposure of personal information (Phone numbers, Usernames).
*   **Digital Footprint Analysis:** Cross-references phone numbers across public sources.
*   **Official Sources:** Indexing of public government gazettes (BOE, Bulletins).
*   **Social Graphing:** Detection of associated accounts on platforms like Spotify, Pinterest, LinkedIn.
*   **Leak Detection:** Checks for potential data exposure in public breaches (Privacy Audit).
*   **Context Mining:** Extracts relevant metadata from public search snippets.

#### 2. 🤖 Service Automation Module (Stress Testing)
Examples of headless browser automation using `Selenium` and `Undetected-Chromedriver`.
*   **Form Interaction:** Automated filling and verification of web forms.
*   **Captcha Handling:** Research on automated challenge detection.
*   **Multi-Threaded Execution:** Demonstrates parallel processing capabilities for high-throughput tasks.
*   **Proxy Management:** Implementation of rotation logic for connection stability.

#### 3. 🛠️ Professional Architecture
*   **Visual Interface:** Modern GUI built with `CustomTkinter`.
*   **Auto-Update System:** Self-updating binary mechanism integrated with GitHub Releases.
*   **Robust Build System:** Automated compilation pipeline for standalone executable generation.

---

### 🚀 Installation & Usage

#### Prerequisites
*   Python 3.11 or higher
*   Google Chrome (for automation modules)

#### Quick Start (Source Code)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kevinkgp92/wannacallbot.git
    cd wannacallbot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If you encounter specific missing modules, run `tools/install_deps.py`)*

3.  **Run the application:**
    ```bash
    python gui.py
    ```

#### Developers / Builders
To generate a standalone executable (.exe):
1.  Ensure you have the correct Python environment active.
2.  Run the build script:
    ```bash
    python build_pro.py
    ```
3.  The executable will appear in the `dist/` folder.

---

## 🛡️ Privacy & Security Notes
*   **Local Processing:** All data aggregation is performed locally on your machine. No data is sent to third-party tracking servers by this software.
*   **Filesystem Safety:** The application uses isolated directories for logs and temporary files, ensuring clean operation and removal.

---

## 🤝 Contributing
Contributions are welcome for features that enhance the **privacy auditing** or **educational value** of the tool. 
*   Please do not submit modules designed for harassment, spam, or malicious activity.
*   All pull requests must adhere to the educational code of conduct.

---
*Built with ❤️ and ⚖️ for the Security Community.*