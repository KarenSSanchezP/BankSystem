# BankSystem

Una aplicación de consola que simula un sistema bancario completo con funcionalidades de gestión de usuarios, cuentas bancarias y análisis de datos con detección de anomalías. El proyecto combina programación orientada a objetos con análisis de datos utilizando herramientas de visualización avanzada.

## Descripción

**BankSystem** es un proyecto colaborativo que implementa un sistema de gestión bancaria con dos roles principales:
- **Cliente**: Gestiona sus cuentas, consulta saldos, realiza depósitos, retiros y transferencias
- **Administrador**: Gestiona usuarios, cuentas, bloqueos de cuentas y análisis de datos con detección de anomalías

## Características principales

### Para Clientes
- Consultar saldo de cuentas
- Visualizar historial de movimientos
- Realizar depósitos
- Realizar retiros
- Transferencias entre cuentas
- Gestión segura de sesión

### Para Administradores
- Crear nuevos clientes
- Crear y gestionar cuentas bancarias
- Bloquear/desbloquear cuentas
- Listar usuarios y cuentas del sistema
- Análisis avanzado de datos con detección de anomalías
- Detección de patrones de lavado de dinero 

### Características de Análisis de Datos
- **Z-Score**: Detección de transacciones inusualmente grandes
- **Structuring**: Identificación de múltiples depósitos pequeños sospechosos
- **Actividad Nocturna**: Análisis de transferencias fuera de horario bancario
- **Grafos**: Detección de cuentas que actúan como centros de distribución (usando NetworkX)

## Requisitos
- Python 3.8 o superior
- Las dependencias están listadas en `requirements.txt`

## Instalación

### 1. Clonar el repositorio
```bash
git clone <URL_REPOSITORIO>
cd BankSystem
```

### 2. Crear un entorno virtual (recomendado)
```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Generar datos de prueba
```bash
python seed_generator.py
```

### 5. Ejecutar la aplicación
```bash
python main.py
```

## Estructura General del Proyecto

```
BankSystem/
├── main.py                 # Punto de entrada principal
├── seed_generator.py       # Generador de datos de prueba con anomalías
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Información del proyecto
└── banksystemapp/          # Aplicación estructurada y modular
    ├── data/                  # Datos del sistema
    ├── outputs/               # Archivos de salida
    │   └── plots/             # Gráficos y visualizaciones
    └── src/              # Código fuente principal
        ├── models/       # Modelos de datos
        │   └── cuentas/    # Definiciones de cuentas, transacciones y transferencias
        │   └── usuarios/    # Definiciones de usuarios, clientes y administradores
        ├── repositories/    # Capa de acceso a datos (CSV)
        ├── services/        # Lógica de negocio
        ├── ui/              # Interfaz de usuario (menús)
        └── utils/           # Funciones de utilidad
```

## Arquitectura

El proyecto sigue una estructura modular con las siguientes capas:

| Capa | Descripción | Ubicación |
|------|-------------|-----------|
| **Models** | Definición de clases y entidades | `banksystemapp/src/models/` |
| **Services** | Lógica de negocio | `banksystemapp/src/services/` |
| **Repositories** | Acceso a datos (CSV) | `banksystemapp/src/repositories/` |
| **UI** | Menús e interfaz de usuario | `banksystemapp/src/ui/` |
| **Utils** | Funciones de utilidad | `banksystemapp/src/utils/` |

## Base de Datos

El proyecto utiliza archivos CSV para almacenar datos:

### usuarios.csv
Contiene información de todos los usuarios:
- ID de usuario
- Nombres y apellidos
- DUI (Documento Único de Identidad)
- PIN/Contraseña
- Username
- Rol (Admin/Cliente)

### cuentas.csv
Información de todas las cuentas bancarias:
- ID de cuenta
- DUI del propietario
- Tipo (Ahorro/Corriente)
- Saldo
- Estado (Activa/Bloqueada)

### transacciones.csv
Registro detallado de transacciones:
- ID de transacción
- ID de cuenta
- Tipo (Depósito/Retiro)
- Monto
- Fecha y hora

### transferencias.csv
Registro de transferencias entre cuentas:
- ID de transferencia
- Cuenta origen
- Cuenta destino
- Monto
- Fecha y hora

## 📚 Librerías Utilizadas

### Para Análisis y Manipulación de Datos
| Librería | Versión | Propósito |
|----------|---------|----------|
| **NumPy** | 2.4.2 | Computación numérica y operaciones matriciales |
| **Pandas** | 3.0.1 | Manipulación de datos estructurados |

### Para Visualización
| Librería | Versión | Propósito |
|----------|---------|----------|
| **Matplotlib** | 3.10.8 | Gráficos y visualizaciones estáticas |
| **Seaborn** | 0.13.2 | Visualizaciones estadísticas avanzadas |
| **NetworkX** | 3.6.1 | Análisis y visualización de grafos de transferencias |


## 📊 Datos de Prueba (Seed Generator)
El `seed_generator.py` crea automáticamente datos de prueba con anomalías incluidas para testing:

### 10 Usuarios (1 Admin + 9 Clientes)
- IDs: 1 al 10
- Juan Pérez (Admin)
- 9 clientes con diferentes nombres

### 9 Cuentas Bancarias
- Distributidas entre clientes
- 5 cuentas de Ahorro
- 4 cuentas Corriente
- Saldos variados entre $250 y $5000

### Transacciones Simuladas (Con Anomalías)
- **Z-Score**: Depósito de $800 en C001 (mucho mayor que el promedio de $13)
- **Structuring**: 5 depósitos de $45 en C002 en el mismo día (patrón sospechoso)

### Transferencias Simuladas (Con Anomalías)
- **Actividad Nocturna**: Múltiples transferencias de C003 entre las 11 PM y 3 AM
- **Grafos**: C004 realiza transferencias a 5 cuentas diferentes (patrón de distribución)

## 🔍 Detección de Anomalías

### Z-Score
Identifica transacciones que se desvían significativamente del promedio:
- Cálculo: `z = (valor - media) / desviación_estándar`
- Si |z| > 3: Se considera anomalía

### Structuring
Detecta múltiples depósitos pequeños que evitan reportes requeridos:
- Busca patrones de múltiples transacciones similares
- En periodos cortos de tiempo

### Actividad Nocturna
Identifica transferencias fuera del horario bancario normal:
- Transferencias entre las 22:00 y 06:00

### Análisis de Grafo (NetworkX)
Identifica patrones de red de transferencias:
- **Nodos**: Cuentas bancarias
- **Aristas**: Transferencias entre cuentas
- **Detección de Hubs**: Cuentas que reciben/envían muchas transferencias

## 🛠️ Estado del Proyecto
**Estado**: Finalizado

## Colaboradores
Proyecto colaborativo de la carrera Ingeniería en Sistemas Informáticos de la Universidad de El Salvador, para el curso Python Foundations impartido en la Escuela de Ingeniería de Sistemas Informáticos por Roberto Méndez.
