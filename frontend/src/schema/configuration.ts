import { Command } from "./command";
import { Param } from "./param";

export interface Configuration{
    name: string
    base_url: string
    context_key: string
    headers: Param[]
    insecure: boolean
    proxy: boolean
}