# Red Descentralizada de Nodos - Poema Distribuido

Sistema descentralizado de nodos que almacenan fragmentos de un poema y se comunican entre sí para reconstruir el texto completo. Inspirado en la "Oda a la Alegría" de Friedrich Schiller.

## 📋 Descripción

Este proyecto implementa una red descentralizada de 8 nodos (N0-N7), donde cada nodo almacena un fragmento de un poema con un ID específico. Los nodos están conectados entre sí de manera no centralizada, formando una topología de red donde cada nodo solo conoce a algunos de sus pares (peers).

Cuando un cliente se conecta a cualquier nodo de la red, este propaga la solicitud a través de sus peers para recopilar todos los fragmentos del poema, los ordena por ID y devuelve el poema completo.

### Poema Completo

El poema que se distribuye en la red es:

```
¡Alegría, hermoso destello de los dioses, / hija del Elíseo! / Ebrios de entusiasmo entramos, / diosa celestial, en tu santuario. / Tu hechizo une de nuevo / lo que la acerba costumbre había separado; / todos los hombres vuelven a ser hermanos / allí donde tu suave ala se posa.
```

## 🏗️ Arquitectura

### Topología de la Red

La red está organizada de forma descentralizada con las siguientes conexiones:

```
N0 (ID:2) ──┬── N1 (ID:4)
            │   ├── N3 (ID:5) 
            │   └── N4 (ID:7) ── N7 (ID:6)
            │
            └── N2 (ID:1)
                ├── N5 (ID:3)
                └── N6 (ID:8)
```

### Distribución de Fragmentos

| Nodo | ID | Fragmento del Poema | Peers |
|------|----|--------------------|-------|
| N0 | 2 | "hija del Elíseo!" | N1, N2 |
| N1 | 4 | "diosa celestial, en tu santuario." | N0, N3, N4 |
| N2 | 1 | "¡Alegría, hermoso destello de los dioses," | N0, N5, N6 |
| N3 | 5 | "Tu hechizo une de nuevo" | N1 |
| N4 | 7 | "todos los hombres vuelven a ser hermanos" | N1, N7 |
| N5 | 3 | "Ebrios de entusiasmo entramos," | N2 |
| N6 | 8 | "allí donde tu suave ala se posa." | N2 |
| N7 | 6 | "lo que la acerba costumbre había separado;" | N4 |

## 🚀 Funcionamiento

### Algoritmo de Propagación

1. **Solicitud inicial**: El cliente hace una petición GET a `/frases` en cualquier nodo
2. **Recolección local**: El nodo agrega su propio fragmento a la lista
3. **Propagación**: El nodo consulta a todos sus peers (excepto al nodo que le hizo la solicitud, para evitar loops)
4. **Recursión**: Cada peer repite el proceso con sus propios peers
5. **Agregación**: Los fragmentos se van acumulando en la respuesta
6. **Ordenamiento**: El nodo original ordena todos los fragmentos por ID
7. **Respuesta**: Se devuelve el poema completo concatenado con separadores " / "

### Prevención de Loops

El sistema incluye un parámetro `from` en las peticiones HTTP que indica de qué nodo proviene la solicitud. Cada nodo excluye al nodo origen de sus propagaciones, evitando ciclos infinitos.

## 📁 Estructura del Proyecto

```
nodos/
├── docker-compose.yml    # Configuración de los 8 contenedores
├── Dockerfile           # Imagen base para todos los nodos
├── requirements.txt     # Dependencias Python (Flask, requests)
├── README.md           # Este archivo
├── N0/
│   └── frase.py        # Código del nodo N0
├── N1/
│   └── frase.py        # Código del nodo N1
├── N2/
│   └── frase.py        # Código del nodo N2
├── N3/
│   └── frase.py        # Código del nodo N3
├── N4/
│   └── frase.py        # Código del nodo N4
├── N5/
│   └── frase.py        # Código del nodo N5
├── N6/
│   └── frase.py        # Código del nodo N6
└── N7/
    └── frase.py        # Código del nodo N7
```

## 🛠️ Tecnologías

- **Python 3.10**: Lenguaje de programación
- **Flask**: Framework web para crear las APIs REST
- **Requests**: Librería para comunicación HTTP entre nodos
- **Docker**: Containerización de nodos
- **Docker Compose**: Orquestación de múltiples contenedores

## 📦 Instalación y Uso

### Prerequisitos

- Docker
- Docker Compose

### Ejecución con Docker Compose

1. Clonar el repositorio:
```bash
git clone <tu-repositorio>
cd nodos
```

2. Levantar todos los nodos:
```bash
docker-compose up --build
```

3. Los nodos estarán disponibles en:
   - N0: http://localhost:5000
   - N1: http://localhost:5001
   - N2: http://localhost:5002
   - N3: http://localhost:5003
   - N4: http://localhost:5004
   - N5: http://localhost:5005
   - N6: http://localhost:5006
   - N7: http://localhost:5007

### Ejecución Manual (sin Docker)

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar cada nodo en terminales separadas:
```bash
# Terminal 1
cd N0 && NODE_NAME=N0 NODE_PORT=5000 python frase.py

# Terminal 2
cd N1 && NODE_NAME=N1 NODE_PORT=5001 python frase.py

# ... y así para cada nodo
```

## 🔌 API Endpoints

### GET `/frase`

Obtiene la frase del nodo actual junto con su información.

**Ejemplo:**
```bash
curl http://localhost:5000/frase
```

**Respuesta:**
```json
{
  "nodo": "N0",
  "frase": "hija del Elíseo!",
  "id": 2,
  "peers": ["N1", "N2"]
}
```

### GET `/frases`

Obtiene el poema completo propagando la solicitud por toda la red.

**Ejemplo:**
```bash
curl http://localhost:5000/frases
```

**Respuesta:**
```json
[
  "¡Alegría, hermoso destello de los dioses, / hija del Elíseo! / Ebrios de entusiasmo entramos, / diosa celestial, en tu santuario. / Tu hechizo une de nuevo / lo que la acerba costumbre había separado; / todos los hombres vuelven a ser hermanos / allí donde tu suave ala se posa."
]
```

## 🐳 Docker

### Dockerfile

El `Dockerfile` crea una imagen base con Python 3.10 que:
- Establece `/app` como directorio de trabajo
- Instala Flask y requests
- Ejecuta el archivo `frase.py`

### Docker Compose

El `docker-compose.yml`:
- Define 8 servicios (N0-N7)
- Cada contenedor usa la misma imagen base
- Monta el archivo `frase.py` específico de cada nodo mediante volúmenes
- Expone puertos del 5000 al 5007
- Configura variables de entorno `NODE_NAME` y `NODE_PORT` para cada nodo
- Usa una red bridge por defecto para permitir comunicación entre contenedores

## 📝 Requirements

El archivo `requirements.txt` contiene:
```
flask
requests
```

- **flask**: Framework web para crear los endpoints REST
- **requests**: Para realizar peticiones HTTP entre nodos

## 🧪 Pruebas

Puedes probar el sistema consultando cualquier nodo:

```bash
# Consultar desde N0
curl http://localhost:5000/frases

# Consultar desde N5
curl http://localhost:5005/frases

# Consultar desde N7
curl http://localhost:5007/frases
```

Todos devolverán el mismo poema completo, aunque recorran diferentes caminos en la red.

## 🎯 Características Destacadas

- ✅ **Descentralización**: No existe un nodo maestro, cualquier nodo puede recibir consultas
- ✅ **Tolerancia a fallos**: Si un nodo cae, la red sigue funcionando (aunque puede faltar un fragmento)
- ✅ **Propagación inteligente**: Evita loops infinitos mediante el parámetro `from`
- ✅ **Escalabilidad**: Fácil agregar nuevos nodos modificando las conexiones
- ✅ **Timeout**: Las peticiones entre nodos tienen un timeout de 2 segundos para evitar bloqueos

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la [Licencia MIT](LICENSE).

## 👤 Autor

Tu nombre - [@tu_usuario](https://github.com/tu_usuario)

## 🙏 Agradecimientos

- Inspirado en la "Oda a la Alegría" (An die Freude) de Friedrich Schiller
- Concepto basado en redes peer-to-peer descentralizadas
