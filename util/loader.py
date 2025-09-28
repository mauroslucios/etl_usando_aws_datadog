import json
import boto3
from logs.etl_logger import ETLLogger
from util.config import LOCALSTACK_ENDPOINT, S3_BUCKET, S3_PREFIX, MAX_FILE_SIZE_BYTES

def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

class Loader:
    @staticmethod
    def load_as_chunked_json_to_s3(df, bucket, prefix, max_bytes):
        ETLLogger.log_event(event="Carga S3", action="Início")

        s3 = s3_client()
        approved_iter = df.filter(col("aprovado_para_envio") == True).toLocalIterator()

        batch, batch_bytes, file_index = [], 0, 0

        def flush_batch(batch_list, idx):
            if not batch_list:
                return
            body = ("\n".join(batch_list)).encode("utf-8")
            key = f"{prefix}part-{idx:05d}.json"
            s3.put_object(Bucket=bucket, Key=key, Body=body)
            ETLLogger.log_event(event="Carga S3", action="Upload", result=f"{key} -> {len(batch_list)} registros")

        for row in approved_iter:
            rec = {
                "cliente_id": int(row["cliente_id"]),
                "nome": row["nome"],
                "tipo_pessoa": row["tipo_pessoa"],
                "zona": row["zona"],
                "renda_mensal": float(row["renda_mensal"]) if row["renda_mensal"] else None,
                "valor_total_bens": float(row["valor_total_bens"]) if row["valor_total_bens"] else 0.0,
                "negativado": bool(row["negativado"]) if row["negativado"] else False,
                "motivo": "cliente_agro_pf_ben_ge_300k_nao_negativado",
            }
            j = json.dumps(rec, ensure_ascii=False)
            j_bytes = j.encode
            if batch_bytes + len(j_bytes) > max_bytes:
                flush(batch, file_index)
                file_index += 1
                batch, batch_bytes = [], 0

            batch.append(j)
            batch_bytes += len(j_bytes)

        flush_batch(batch, file_index)
        ETLLogger.log_event(event="Carga S3", result="Finalizada com sucesso")