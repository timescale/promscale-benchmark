import time, random, datetime
from locust import HttpUser, task, constant, tag
from gevent.pool import Group
from requests.adapters import HTTPAdapter

prometheus_remote_write_range_queries = [
  'prometheus_remote_storage_highest_timestamp_in_seconds{} - ignoring(remote_name, url) group_right(instance) (prometheus_remote_storage_queue_highest_sent_timestamp_seconds{} != 0)',
  'clamp_min( rate(prometheus_remote_storage_highest_timestamp_in_seconds{}[5m]) -  ignoring (remote_name, url) group_right(instance) rate(prometheus_remote_storage_queue_highest_sent_timestamp_seconds{}[5m]), 0)',
  'prometheus_remote_storage_shards{}',
  'rate(prometheus_remote_storage_samples_in_total{}[5m]) - ignoring(remote_name, url) group_right(instance) rate(prometheus_remote_storage_succeeded_samples_total{}[5m])',
  'sum(prometheus_sd_discovered_targets{})',
  'sum by (job) (rate(prometheus_target_scrapes_exceeded_sample_limit_total[1m]))',
  'sum by (job) (rate(prometheus_target_scrapes_sample_duplicate_timestamp_total[1m]))',
  'rate(prometheus_remote_storage_samples_dropped_total{}[5m])',
  'sum by (job) (rate(prometheus_target_scrapes_sample_out_of_bounds_total[1m]))',
  'rate(prometheus_tsdb_head_samples_appended_total{}[5m])']

prometheus_range_queries =[
  'prometheus_tsdb_head_chunks{}',
  'prometheus_tsdb_head_series{}',
  'rate(prometheus_engine_query_duration_seconds_count{slice="inner_eval"}[5m])',
  'max by (slice) (prometheus_engine_query_duration_seconds{quantile="0.9"}) * 1e3',
  'sum(rate(prometheus_target_sync_length_seconds_sum{}[5m])) by (scrape_job) * 1e3',
  'rate(prometheus_target_interval_length_seconds_sum{}[5m]) / rate(prometheus_target_interval_length_seconds_count{}[5m]) * 1e3',
  'sum by (job) (rate(prometheus_target_scrapes_exceeded_body_size_limit_total[1m]))',
  'sum by (job) (rate(prometheus_target_scrapes_exceeded_sample_limit_total[1m]))']  

node_exporter_range_queries = [
  'sum by(instance) (irate(node_cpu_seconds_total{mode="system"}[5m])) / on(instance) group_left sum by (instance)((irate(node_cpu_seconds_total{}[5m])))',
  'node_time_seconds{} - node_boot_time_seconds{}',
  'node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"}',
  'node_memory_MemTotal_bytes{job="node-exporter"}',
  'sum by(instance) (irate(node_cpu_seconds_total{job="node-exporter", mode="user"}[5m])) / on(instance) group_left sum by (instance)((irate(node_cpu_seconds_total{job="node-exporter"}[5m])))',
  'sum by(instance) (irate(node_cpu_seconds_total{job="node-exporter", mode="iowait"}[5m])) / on(instance) group_left sum by (instance)((irate(node_cpu_seconds_total{job="node-exporter"}[5m])))',
  'node_memory_MemTotal_bytes{} - node_memory_MemFree_bytes{} - (node_memory_Cached_bytes{} + node_memory_Buffers_bytes{} + node_memory_SReclaimable_bytes{})',
  'node_memory_MemFree_bytes{}',
  'irate(node_network_receive_bytes_total{job="node-exporter"}[5m])*8',
  'sum by(instance) (irate(node_cpu_guest_seconds_total{mode="user"}[5m])) / on(instance) group_left sum by (instance)((irate(node_cpu_seconds_total{}[5m])))']

# Simulating one scenario
# Additional scenarios can be added into separate classes or just by adding
# additional task into this class. Each task should be tagged to enable filtering
# for different scenarios
class GrafanaScenario1(HttpUser):
  def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount('https://', HTTPAdapter(pool_maxsize=50))
        self.client.mount('http://', HTTPAdapter(pool_maxsize=50))

  wait_time = constant(15) # heuristically picked value

  def run_range_queries(self, start, end, step, queries):
    url = '/api/v1/query_range?query={promql}&start={start}&end={end}&step={step}'
    reqs = []
    for query in queries:
        reqs.append(url.format(promql=query, start=start, end=end, step=step))
    self.send_reqs(reqs)

  def run_queries(self, queries):
    url = '/api/v1/query?query={promql}'
    reqs = []
    for query in queries:
          reqs.append(url.format(promql=query))
    self.send_reqs(reqs)

  def send_reqs(self, reqs):
    group = Group()
    def sendReq(query):
      print(query) # NOTE: used for debugging and should be removed once we have confidence in queries
      resp = self.client.get(query)
      print(resp.status_code, resp.text) # NOTE: used for debugging and should be removed once we have confidence in queries
    # This will spawn the number of queries needed in parallel
    for req in reqs:
          group.spawn(sendReq(req))
    group.join()

  @tag('instant')
  @task(3)
  def test_dashboard_instant_queries(self):
    instant_queries = ['count by (job, instance, version) (prometheus_build_info{})',
      'max by (job, instance) (time() - process_start_time_seconds{})',
      'max by (mountpoint) (node_filesystem_avail_bytes{job="node-exporter", fstype!=""})',
      'max by (mountpoint) (node_filesystem_size_bytes{job="node-exporter", fstype!=""})']
    
    self.run_queries(queries=instant_queries)

  @tag('last3h')
  @task(3) # this task runs 3x more often then 12h queries
  def test_dashboard_range_queries_last3h(self):
    start = int(time.time()) - (3600*3)
    end = int(time.time())
    self.run_range_queries(start=start, end = end, step = 30, queries=prometheus_remote_write_range_queries)

  @tag('last1h')
  @task(3)
  def test_dashboard_range_queries_last1h(self):
    start = int(time.time()) - 3600
    end = int(time.time())
    self.run_range_queries(start = start, end=end, step=30, queries=prometheus_range_queries)

  @tag('last12h')
  @task(1)
  def test_dashboard_range_queries_last12h(self):
    start = int(time.time()) - (3600*12)
    end = int(time.time())
    self.run_range_queries(start=start, end=end, step = 60, queries=node_exporter_range_queries)

  @tag('random1h')
  @task(1)
  def test_dashboard_random1h(self):
    random_hour = random.uniform(1, 12)
    start = int(time.time()) - datetime.timedelta(hours=random_hour)
    end = start + 3600
    self.run_range_queries(start=start, end=end, step = 60, queries=node_exporter_range_queries)
