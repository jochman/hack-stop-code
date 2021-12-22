import { Param } from "./param";

export interface Command{
    name: string
    method: string
    suffix: string
    params: Param[]
    headers: Param[]
    body: string
}