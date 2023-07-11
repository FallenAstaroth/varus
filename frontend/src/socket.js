import {io} from "socket.io-client";
import {backendUrl} from "@/globals";


export const socket = io(backendUrl, { withCredentials: true });