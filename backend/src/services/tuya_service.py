import json
from time import sleep
from pathlib import Path
from tinytuya import BulbDevice, scan
from src.models.dispositivo_model import DispositivoInfo
from src.services.controlador_service import ControladorService
from concurrent.futures import ThreadPoolExecutor, as_completed

def realizar_varredura() -> list[DispositivoInfo] | None:

    """
    
    💡 Realiza uma varredura na rede usando scan() para detectar dispositivos compatíveis e verifica se algum dispositivo foi encontrado.

        ⚙️ Funcionamento:
            1. Chama a função scan() da biblioteca Tinytuya para realizar uma varredura na rede em busca de dispositivos compatíveis.
            2. Lê o snapshot.json usando a função obter_dispositivos() para obter a lista de dispositivos salvos.
            3. Verifica se a lista de dispositivos obtida do snapshot.json está vazia ou não.
            4. Retorna a lista de dispositivos encontrados se houver dispositivos salvos, ou None caso contrário.

        🎁 Retornos:
            - list[DispositivoInfo] | None: Uma lista de objetos DispositivoInfo representando os dispositivos encontrados, ou None se não houver dispositivos.

    """

    try:

        scan()

        sleep(15)

        snapshot: list = obter_dispositivos()

        if not snapshot: return None

        else: return snapshot

    except Exception as e:

        raise Exception("Ocorreu um erro durante a varredura: " + str(e))

def obter_dispositivos() -> list[DispositivoInfo]:
    
    """
    
    💡 Lê o arquivo snapshot.json e retorna a lista de informações dos dispositivos salvos.

        ⚙️ Funcionamento:
            1. Constrói o caminho para o arquivo snapshot.json usando o módulo pathlib.
            2. Abre o arquivo snapshot.json em modo de leitura.
            3. Carrega o conteúdo do arquivo usando json.load() e extrai a lista de dispositivos.
            4. Retorna a lista de dispositivos.
    
        ⁉️ Raises:
            - *FileNotFoundError*: Caso o arquivo snapshot.json não seja encontrado.
            - *ValueError*: Se o arquivo snapshot.json contiver um formato inválido.
            - *Exception*: Para quaisquer outros erros que possam ocorrer durante a leitura do arquivo.

        🎁 Retornos:
            - list[DispositivoInfo]: Uma lista de objetos DispositivoInfo representando os dispositivos salvos no snapshot.json.

    """

    try:

        path = Path(__file__).resolve().parent.parent / 'snapshot.json'

        with open(path, 'r') as f:

            data = json.load(f)

            devices = data.get('devices', [])

            dispositivos = []

            for device in devices:

                dispositivo_info = DispositivoInfo(

                    id=device.get('id', ''),
                    name=device.get('name', ''),
                    ip=device.get('ip', None),
                    key=device.get('key', ''),
                    ver=device.get('ver', None)

                )

                dispositivos.append(dispositivo_info)

            return dispositivos

    except FileNotFoundError as e: raise FileNotFoundError("O arquivo snapshot.json não foi encontrado.")
    except json.JSONDecodeError as e: raise ValueError("O arquivo snapshot.json contém um formato inválido.")
    except Exception as e: raise Exception("Ocorreu um erro ao ler o arquivo snapshot.json: " + str(e))

def _criar_bulbdevice( info: DispositivoInfo ) -> tuple[str , str, BulbDevice] | None:

    """
    
    💡 Cria um objeto BulbDevice a partir de um objeto DispositivoInfo ( obtido do snapshot.json ).

        ⚙️ Funcionamento:
            1. Recebe um objeto DispositivoInfo contendo as informações do dispositivo (id, ip, key, ver).
            2. Tenta criar um objeto BulbDevice ( da biblioteca da Tinytuya ) usando as informações fornecidas.
            3. Configura a versão e a persistência do socket do BulbDevice.
            4. Retorna o objeto BulbDevice criado.

        🧩 Parâmetros:
            - info (DispositivoInfo): Um objeto DispositivoInfo contendo as informações do dispositivo, com as seguintes chaves: id, ip, key, ver.

        🎁 Retornos:
            - tuple[str, str, BulbDevice]: Uma tupla contendo o id do dispositivo, o nome do dispositivo e o objeto BulbDevice criado a partir das informações fornecidas. O objeto BulbDevice será None se ocorrer um erro durante a criação ou configuração do dispositivo.
            - None: Se ocorrer um erro durante a criação do objeto BulbDevice ou ao configurar o dispositivo.
            
    """

    try:

        bulb = BulbDevice(info.id, info.ip, info.key)
        bulb.set_version(info.ver)
        bulb.set_socketPersistent(True)

        return (info.id, info.name, bulb)
    
    except Exception as e: return None

def _criar_controlador( info: DispositivoInfo ) -> ControladorService | None:

    """
    
    💡 Cria um objeto ControladorService a partir de um objeto DispositivoInfo ( obtido do snapshot.json ).

        ⚙️ Funcionamento:
            1. Recebe um objeto DispositivoInfo contendo as informações do dispositivo (id, ip, key, ver).
            2. Tenta criar um objeto ControladorService usando as informações fornecidas.
            3. Retorna o objeto ControladorService criado.

        🧩 Parâmetros:
            - info (DispositivoInfo): Um objeto DispositivoInfo contendo as informações do dispositivo, com as seguintes chaves: id, ip, key, ver.

        🎁 Retornos:
            - ControladorService: Um objeto ControladorService criado a partir das informações fornecidas.
            - None: Se ocorrer um erro durante a criação do objeto ControladorService ou ao configurar o dispositivo.

    """

    try:

        tuya_device = _criar_bulbdevice(info)

        if tuya_device[2] is None: return None

        controlador = ControladorService( tuya_device )

        return controlador
    
    except Exception as e: return None

def criar_controladores( infos: list[DispositivoInfo | None] ) -> list[ControladorService | None]:

    """
    
    💡 Cria objetos ControladorService para cada objeto DispositivoInfo fornecido e retorna uma lista desses objetos.

        ⚙️ Funcionamento:
            1. Recebe uma lista de objetos DispositivoInfo ( infos ) como parâmetro.
            2. Inicializa uma lista de ControladorService com o mesmo tamanho da lista de DispositivoInfo.
            3. Utiliza ThreadPoolExecutor para criar objetos ControladorService em paralelo, chamando a função criar_controlador() para cada objeto DispositivoInfo.
            4. Armazena os objetos ControladorService criados na lista de controladores, mantendo a ordem original dos DispositivoInfo.
            5. Retorna a lista de objetos ControladorService criados.

        🧩 Parâmetros:
            - infos (list[DispositivoInfo | None]): Uma lista de objetos DispositivoInfo para os quais os ControladorService serão criados.

        🎁 Retornos:
            - list[ControladorService | None]: Uma lista de objetos ControladorService criados a partir dos objetos DispositivoInfo fornecidos.

    """
    
    controladores: list[ControladorService | None] = [None] * len(infos)

    with ThreadPoolExecutor(max_workers=10) as executor:

        futures = {}

        for i, info in enumerate(infos):

            future = executor.submit(_criar_controlador, info)

            futures[future] = i

        for future in as_completed(futures):

            i = futures[future]

            controladores[i] = future.result()

    return controladores