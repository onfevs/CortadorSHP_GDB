# Recorte Automático de Cartografía Base para Proyectos Ambientales y/o Mineros

**Versión:** 1.0.0  
**Autor:** Jorge Vallejo [@OnfeVS](https://github.com/OnfeVS)  
**Fecha de Última Actualización:** 2024-01-28  
**Licencia:** MIT  

---

## 📋 Descripción

Este script automatiza el recorte de una base de datos geográfica (GDB) utilizando un área de recorte definida por un shapefile. Está diseñado específicamente para preparar la cartografía base que debe presentarse ante entidades como la **ANM (Agencia Nacional de Minería)** o la **ANLA (Autoridad Nacional de Licencias Ambientales)** en el marco de proyectos como:

- Informes de **ICA (Informe de Cumplimiento Ambiental)**.
- Estudios de **EIA (Estudio de Impacto Ambiental)**.
- Plan de **PMA (Plan de Manejo Ambiental)**.
- Formatos de **FBM (Formatos Basicos Mineros)**.
- Programas **PUEE Programa Único de Exploración y Explotación**.
- Plan de **PTE Plan de Trabajo de Explotación**.
- Programas de **PTO (Plan de Trabajo y Obras)**.

La cartografía base procesada se debe incluir en una carpeta adicional donde también se encuentre la GDB de **Cartografía Temática**, facilitando su integración en otros análisis geoespaciales.

---

## 🛠️ Funcionalidades

- **Recorte de capas:** Recorta todas las capas vectoriales (Feature Classes) en la raíz de la GDB utilizando un shapefile como área de recorte.
- **Procesamiento de Feature Datasets:** Identifica y recorta recursivamente las capas contenidas en Feature Datasets.
- **Validación de datos:** Excluye automáticamente las capas sin intersección con el área de recorte o las que quedan vacías tras el proceso.
- **Gestión de resultados:** Genera automáticamente una nueva GDB con un nombre único para almacenar las capas recortadas.
- **Eliminación de archivos innecesarios:** Limpia archivos temporales generados por el proceso.
- **Optimización de tiempo:** Reduce significativamente el tiempo necesario para realizar estas tareas de manera manual.

---

## 📂 Estructura de la GDB de Salida

La GDB generada sigue el formato estándar para reportes y contiene:

1. **Cartografía Base:**  
   Incluye todas las capas recortadas esenciales para los informes y análisis ambientales.
   
2. **Cartografía Temática:**  
   Puede agregarse posteriormente según los requerimientos específicos del proyecto.

---

## 🚀 Cómo Usar el Script

### 1️⃣ **Requisitos Previos**
- Tener instalado **ArcGIS** con la extensión **ArcPy** configurada.
- Contar con:
  - La GDB que contiene las capas a recortar.
  - Un shapefile con el área de recorte.
- Asegurarse de que la ruta de entrada de la GDB y el shapefile sean accesibles.

### 2️⃣ **Pasos para Ejecutar**
1. **Descargar el script** desde este repositorio.
2. Abre tu terminal o consola de Python y ejecuta el script con:
   ```bash
   python recortar_gdb.py
   ```
3. **Proporcionar las rutas** cuando el script lo solicite:
   - Ruta de la GDB de entrada.
   - Ruta del shapefile para el recorte.
4. El script generará automáticamente una nueva GDB en la misma carpeta que la GDB de entrada.

### 3️⃣ **Salida Generada**
- Una nueva GDB con el formato `CartoBase_X.gdb` que contiene todas las capas recortadas.

---

## 📌 Consideraciones

- **Validación previa:** Asegúrate de que los datos en la GDB de entrada estén correctamente organizados y georreferenciados.
- **Sistema de referencia espacial:** El shapefile de recorte y las capas en la GDB deben estar en el mismo sistema de coordenadas. De lo contrario, puede haber problemas en el recorte.

---

## 📈 Ejemplo de Uso

1. Ruta de la GDB de entrada: `C:\Proyectos\ICA\CartografiaBase.gdb`
2. Ruta del shapefile de recorte: `C:\Proyectos\ICA\AreaDeRecorte.shp`
3. Resultado esperado:
   - Nueva GDB: `C:\Proyectos\ICA\CartoBase_1.gdb`
   - Contenido:
     ```
     CartoBase_1.gdb/
     ├── Capas_Raiz/
     │   ├── Hidrografia
     │   ├── Carreteras
     │   └── UsoDelSuelo
     └── Feature_Datasets/
         ├── Geologia/
         │   ├── Fallas
         │   ├── Rocas
         └── Ecosistemas/
             ├── Bosques
             └── Humedales
     ```

---

## 🔧 Personalización

Si necesitas ajustar el script para adaptarlo a otros requisitos (por ejemplo, agregar nuevas capas, generar reportes adicionales, etc.), no dudes en contactarme.

---

## 📬 Contacto

Si tienes dudas, sugerencias o mejoras para el script, ¡estoy encantado de escuchar! Puedes contactarme aquí:

- **Nombre:** Jorge Vallejo  
- **GitHub:** [@OnfeVS](https://github.com/OnfeVS)  
- **Instagram:** [@OnfeVS](https://www.instagram.com/onfevs/)  

---

## 📄 Créditos y Licencia

- **Autor:** Jorge Vallejo [@OnfeVS](https://github.com/OnfeVS)  
- **Licencia:** Este proyecto está licenciado bajo la [Licencia MIT](LICENSE). Si usas este script, por favor da el crédito correspondiente.

**¡Gracias por usar este script! Espero que te ahorre tiempo y facilite tu trabajo. 🚀**
