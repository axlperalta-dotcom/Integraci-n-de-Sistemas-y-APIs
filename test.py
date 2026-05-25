import urllib.request
import urllib.error
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "http://127.0.0.1:8000/query"
headers = {
    "Content-Type": "application/json",
    "X-API-Key": "my-secret-token"
}

def make_request(question, use_auth=True):
    data = json.dumps({"question": question}).encode("utf-8")
    req_headers = headers.copy()
    if not use_auth:
        del req_headers["X-API-Key"]
        
    req = urllib.request.Request(url, data=data, headers=req_headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            res_data = response.read().decode("utf-8")
            print(f"[{response.status}] Success for '{question}':")
            print(json.dumps(json.loads(res_data), indent=2))
            print("-" * 40)
    except urllib.error.HTTPError as e:
        res_data = e.read().decode("utf-8")
        print(f"[{e.code}] Error for '{question}':")
        try:
            print(json.dumps(json.loads(res_data), indent=2))
        except:
            print(res_data)
        print("-" * 40)

print("--- Iniciando Pruebas de la API ---\n")

print("Prueba 1: Sin API Key (Debería fallar)")
make_request("¿Cuántos empleados hay?", use_auth=False)

print("Prueba 2: Consulta segura normal")
make_request("¿Cuántos empleados hay en ingeniería?")

print("Prueba 3: Consulta intentando acceder a SSN (Muestra enmascaramiento)")
make_request("Dame el seguro social de todos")

