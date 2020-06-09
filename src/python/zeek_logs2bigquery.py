from google.cloud import bigquery
import os
import time
from zat.log_to_dataframe import LogToDataFrame


GCP_SERVICE_ACCOUNT_JSON = "/Users/romainburgot/cyber-258808-5770ac602d65.json"
DATA_IN = "/Volumes/ELEMENTS/downlods/CICIDS-2017/zeek_logs"


class JobQueue(object):
    max_nb_job = 30
    sleeping_time = 2
    job_queue = []
    finished_jobs = []

    def add_job(self, job):
        while len(self.job_queue) >= self.max_nb_job:
            for j in self.job_queue:
                if not j.running():
                    break
            else:
                j = None
            if j is not None:
                self.finished_jobs.append(j)
                self.job_queue.remove(j)
            time.sleep(self.sleeping_time)
        self.job_queue.append(job)


if __name__ == "__main__":
    client = bigquery.Client.from_service_account_json(GCP_SERVICE_ACCOUNT_JSON)
    log_to_df = LogToDataFrame()
    jq = JobQueue()
    for root, directories, files in os.walk(DATA_IN):
        for f in files:
            if f.endswith(".log"):
                table_id = "cyber-258808.cicids_2017." + f.replace(".", "_")
                df = log_to_df.create_dataframe(os.path.join(root, f))
                df.reset_index(inplace=True)
                for c, t in df.dtypes.iteritems():
                    # print((c, str(t)))
                    if str(t) == "timedelta64[ns]":
                        df[c] = df[c].dt.total_seconds()
                    elif str(t).endswith("[ns]"):
                        df[c] = df[c].astype(str(t).replace("[ns]", "[ms]"))
                        # accepting to loose precision because of pyarrow that would otherwise not be happy
                        # TODO? Better?
                    elif str(t) == "category":
                        df[c] = df[c].astype(str)
                df.rename(
                    columns=dict(
                        [(c, c.lower().replace(".", "_")) for c in df.columns]
                    ),
                    inplace=True,
                )
                job = client.load_table_from_dataframe(df, table_id)
                jq.add_job(job)
                pass

        # if root.endswith(".parquet"):
        #     for f in files:
        #         if f.endswith(".parquet") :
        #             table_id = 'cyber-258808.cicids_2017.' + os.path.split(root)[1][:-len('.parquet')].replace('.', '_')
        #             with open(os.path.join(root, f), "rb") as parquet_file:
        #                 j = client.load_table_from_file(parquet_file, table_id)
        #                 print(j.result())
        #             pass


# from .utils import run_cmd
#
# import pandas as pd
#
# df = pd.DataFrame()
# df.to_gbq()
#
# FILE = "/Volumes/ELEMENTS/downlods/CICIDS-2017/zeek_logs/CICIDS2017_Friday-WorkingHours.pcap.zeek.logs/conn.log"
#
#
# # gsutil -m cp -R "/Volumes/ELEMENTS/downlods/CICIDS2018/nfdump_netflow/*.zip" "gs://cybair_shared/CICIDS2018/nfdump_netflow"
# # gsutil -m cp -R "/Volumes/ELEMENTS/downlods/CICIDS2018/windows_log_events/*.zip" "gs://cybair_shared/CICIDS2018/windows_log_events"
#
#
# def split_headers(l):
#     field_names = l.split('\t')
#     del field_names[0]
#     field_names[-1] = field_names[-1][:-1]
#     return [fn.replace('.', '_') for fn in field_names]
#
#
# TYPES_DICT = {
#     "count": "INT64",
#     "enum": "INT64",
#     "port": "INT64",
#     "addr": "STRING",
#     "string": "STRING",
#     "time": "TIMESTAMP",
#     "bool": "BOOL",
#     "interval": "FLOAT64"
# }
#
#
# def get_bigquery_type(zeek_type):
#     if zeek_type.startswith("set["):
#         return "ARRAY<%s>" % get_bigquery_type(zeek_type.split('[')[1][:-1])
#     return TYPES_DICT[zeek_type]
#
#
# def get_schema(zeek_file):
#     lines2skip = 0
#     with open(zeek_file) as f:
#         l = f.readline()
#         lines2skip += 1
#         while not l.startswith("#fields"):
#             print("Skipping: <%s>" % l)
#             l = f.readline()
#             lines2skip += 1
#         field_names = split_headers(l)
#         l = f.readline()
#         lines2skip += 1
#         assert l.startswith("#types")
#         field_types = split_headers(l)
#         schema = dict()
#         for n, t in zip(field_names, field_types):
#             schema["name"] = n
#             schema["type"] = get_bigquery_type(t)
#     return schema, lines2skip
#
#
# if "__name__" == "__main__":
#     pass
