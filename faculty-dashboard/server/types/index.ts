export interface KpForecastItem {
  time_tag: string
  kp: number
  observed: string
  noaa_scale: string | null
}

export interface AceSwepamItem {
  time_tag: string
  dsflag: number
  dens: number
  speed: number
  temperature: number
}

export interface AceMagItem {
  time_tag: string
  dsflag: number
  numpts: number
  gse_bx: number
  gse_by: number
  gse_bz: number
  gse_lat: number
  gse_lon: number
  gsm_bx: number
  gsm_by: number
  gsm_bz: number
  gsm_lat: number
  gsm_lon: number
  bt: number
}

export interface ProtonFluxItem {
  time_tag: string
  satellite: number
  flux: number
  energy: string
  yaw_flip: number
  channel: string
}

export interface XrayFluxItem {
  time_tag: string
  satellite: number
  flux: number
  observed_flux: number
  electron_correction: number
  electron_contaminaton: boolean
  energy: string
}
