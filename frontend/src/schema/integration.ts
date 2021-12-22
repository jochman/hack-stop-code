import { Command } from "./command";
import { Configuration } from "./configuration";

export interface Integartion{
    configuration: Configuration
    commands: Command[]
}