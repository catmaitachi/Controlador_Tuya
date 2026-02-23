from tinytuya import BulbDevice
from src.models.dispositivo_model import Cor, Branco, DispositivoState

class ControladorService:

    def __init__(self, tuya_device: tuple[str, str, BulbDevice]):

        self._id = tuya_device[0]
        self._name = tuya_device[1]
        self._bulb = tuya_device[2]
        self._conexao: bool = False
        self._memoria: DispositivoState | None = None

    def obter_id(self) -> str:

        return self._id
    
    def obter_nome(self) -> str:

        return self._name

    def obter_bulb(self) -> BulbDevice:

        return self._bulb

    def obter_brilho(self) -> int:

        try: return self._bulb.get_brightness_percentage()

        except Exception as e: 
            
            self.testar_conexao()

            raise Exception("Não foi possível obter o brilho do dispositivo. Verifique a conexão e tente novamente.")

    def definir_brilho(self, porcentagem: int = 100):

        try:

            self._bulb.set_mode('white', True)
            self._bulb.set_brightness_percentage(porcentagem)

            self._salvar_estado()

        except Exception as e:

            self.testar_conexao()
            
            raise Exception("Não foi possível definir o brilho do dispositivo. Verifique a conexão e tente novamente.")

    def obter_temperatura(self) -> int:

        try: return self._bulb.get_colourtemp_percentage()

        except Exception as e: 
            
            self.testar_conexao()

            raise Exception("Não foi possível obter a temperatura do dispositivo. Verifique a conexão e tente novamente.")

    def definir_temperatura(self, temperatura: int = 100):

        try:

            self._bulb.set_mode('white', True)    
            self._bulb.set_colourtemp_percentage(temperatura) 

            self._salvar_estado()

        except Exception as e:

            self.testar_conexao()

            raise Exception("Não foi possível definir a temperatura do dispositivo. Verifique a conexão e tente novamente.")
    
    def obter_cor(self) -> tuple[int, int, int]:

        try: return self._bulb.colour_rgb()

        except Exception as e:

            self.testar_conexao()

            raise Exception("Não foi possível obter a cor do dispositivo. Verifique a conexão e tente novamente.")
    
    def definir_cor(self, r: int = 255, g: int = 255, b: int = 255):
        
        if r == 0 and g == 0 and b == 0: self.desligar()

        else:

            try:

                self._bulb.set_mode('colour', True)
                self._bulb.set_colour(r, g, b)

            except Exception as e:

                self.testar_conexao()

                raise Exception("Não foi possível definir a cor do dispositivo. Verifique a conexão e tente novamente.")

            self._salvar_estado()

    def obter_modo(self) -> str:

        try: return self._bulb.get_mode()

        except Exception as e: 
            
            self.testar_conexao()

            raise Exception("Não foi possível obter o modo do dispositivo. Verifique a conexão e tente novamente.")

    def _salvar_estado(self):

        try:

            if self._bulb.get_mode() == 'white':
                
                temperatura = self._bulb.get_colourtemp_percentage()
                brilho = self._bulb.get_brightness_percentage()

                branco = Branco( temperatura=temperatura, brilho=brilho )

                self._memoria = DispositivoState( modo='white', branco=branco )

            elif self._bulb.get_mode() == 'colour':

                r, g, b = self._bulb.colour_rgb()

                colorido = Cor( r=r, g=g, b=b )

                self._memoria = DispositivoState( modo='colour', cor=colorido )

        except Exception as e:

            print("Não foi possível salvar o estado do dispositivo")

    def recuperar_estado(self):

        try:

            if self._memoria:

                if self._memoria.modo == 'white' and self._memoria.branco:

                    self.definir_brilho(self._memoria.branco.brilho)
                    self.definir_temperatura(self._memoria.branco.temperatura)

                elif self._memoria.modo == 'colour' and self._memoria.cor:

                    self.definir_cor(self._memoria.cor.r, self._memoria.cor.g, self._memoria.cor.b)

        except Exception as e:

            print("Não foi possível recuperar o estado do dispositivo")

    def desligar(self):
        
        try: self._bulb.set_brightness_percentage(0)

        except Exception as e:

            self.testar_conexao()

            raise Exception("Não foi possível desligar o dispositivo. Verifique a conexão e tente novamente.")

    def testar_conexao(self) -> bool:

        try:

            self._bulb.state()
            self._conexao = True
        
        except Exception as e: self._conexao = False