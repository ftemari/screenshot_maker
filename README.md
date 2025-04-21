
# 📸 Video Screen Extractor

Este script en Python permite analizar videos `.mp4` (por ejemplo, grabaciones de pantalla de dispositivos) y generar **capturas de pantalla automáticas** por cada cambio significativo de pantalla.

Ideal para flujos de diseño o documentación en Figma.

---

## 🧠 ¿Qué hace?

- Procesa **todos los videos** dentro de la carpeta `videos/`.
- Genera capturas de pantalla cada vez que detecta un cambio visual (utilizando SSIM - Structural Similarity).
- Nombra cada screenshot usando este formato:

  ```
  <nombre-del-video>_<número>_<minutos>m<segundos>s.png
  ```

  Ejemplo: `miapp_001_00m15s.png`

- Elimina capturas muy parecidas entre sí para dejar solo una por pantalla.
- Si se vuelve a correr el script, **borra solo las capturas del video que se está procesando de nuevo**, sin afectar las de otros videos.

---

## 📁 Estructura del proyecto

```
.
├── extract_screens.py        ← Script principal
├── videos/                   ← Colocá aquí tus archivos .mp4
└── screenshots/              ← Acá se generan las capturas
```

---

## 🛠️ Requisitos

- Python 3.7 o superior

### Instalación de dependencias

```bash
pip install opencv-python scikit-image
```

---

## 🚀 Cómo usarlo

### 1. Clonar el repositorio o copiar los archivos

```bash
git clone <repo-url>
cd <nombre-del-repo>
```

### 2. (Opcional) Crear un entorno virtual

```bash
python3 -m venv env
source env/bin/activate          # En Mac/Linux
# o en Windows:
# env\Scripts\activate
```

### 3. Instalar las dependencias necesarias


```bash
pip install -r requirements.txt
```

### 4. Colocar los archivos de video

Agregá tus archivos `.mp4` dentro de la carpeta `videos/`.  
El nombre del archivo de video se usará como prefijo para los screenshots.

### 5. Ejecutar el script

```bash
python screenshot_maker.py
```

---

## ✅ Resultado

- Los screenshots se guardarán en la carpeta `screenshots/`.
- Cada uno tendrá el nombre del video, un número secuencial, y el minuto/segundo del video en que se generó.
- Las capturas repetidas o demasiado parecidas se eliminarán automáticamente.

---

## 🧪 Ejemplo de uso

Si tenés un video llamado `loginflow.mp4` en la carpeta `videos/`, y lo ejecutás, se generarán imágenes como:

```
screenshots/
├── loginflow_001_00m02s.png
├── loginflow_002_00m07s.png
└── loginflow_003_00m12s.png
```

---

## 🧼 ¿Qué pasa si vuelvo a correrlo?

El script:
- Detecta qué videos ya tienen screenshots generadas.
- Elimina esas imágenes **antes** de volver a generarlas.
- Así evitás duplicados y podés actualizar capturas fácilmente sin afectar los otros videos procesados.

---

## 🔧 Personalización

Si querés ajustar la sensibilidad:
- Para que detecte **más cambios** → bajá el `threshold` de SSIM (`threshold=0.95`)
- Para que detecte **menos cambios** → subilo (por ejemplo `0.98`)

También podés modificar:
- La lógica de detección de similitud entre capturas (`similarity_threshold=0.98`)
- El formato de los nombres de archivos
- El orden o ubicación de salida

---

## 🧑‍💻 Autor

Hecho con 💻 y 🧠 por [Tu Nombre o Equipo].
# screenshot_maker
