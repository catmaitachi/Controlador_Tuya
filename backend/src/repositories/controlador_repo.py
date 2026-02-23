import threading
from src.services.controlador_service import ControladorService
from src.services.tuya_service import obter_dispositivos, criar_controladores, realizar_varredura

class ControladorRepo:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):

        with cls._lock:

            if cls._instance is None:

                cls._instance = super().__new__(cls)
                cls._instance._controladores= {}
                cls._instance._carregar_controladores()

        return cls._instance

    def _carregar_controladores(self) -> dict[str, ControladorService]:

        if not self._controladores:

            controladores = criar_controladores( obter_dispositivos() )

            if controladores:

                for controlador in controladores:

                    if controlador is not None:

                        self._controladores[controlador.obter_id()] = controlador

        return self._controladores
    
    def obter_por_id(self, id: str) -> ControladorService | None:

        controladores = self._carregar_controladores()

        if id in controladores: return controladores[id]
        else: return None

    def obter_todos(self) -> list[ControladorService]:

        controladores = self._carregar_controladores()

        return list(controladores.values())
    
    def atualizar_controladores(self) -> list[ControladorService] | None:

        realizar_varredura()

        self._controladores = {}
        
        return self._carregar_controladores()