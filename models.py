from pydantic import BaseModel


class Azienda(BaseModel):
    nomeAzienda: str
    indirizzoResidenzaFiscale: str
    indirizzoResidenzaCitta: str
    pIva: str


class Fattura(BaseModel):
    numeroFattura: str
    nominativo: str
    indirizzoResidenza: str
    capResidenza: str
    cittaResidenza: str
    pIva: str
    codFiscale: str
    lavoroSvolto: str
    totale: str
    theme: str


class Body(BaseModel):
    azienda: Azienda
    fattura: Fattura