import axios from 'axios'
import {BE_BASE_URL} from "@/constants/http/api";

const axiosInstance = axios.create({
  baseURL: BE_BASE_URL,
  timeout: 10000,
});

export default axiosInstance;