
import threading


class DownstreamAPI():

	def __init__(self, db):
		# For this question, I simplify the API to just read from a dict
		self.db = db

	def call(self, member_id):
		return self.db[member_id]


class NirvanaAPI():


	def __init__(self, coalesceStrategy, downstreamAPIs):
		self.coalesceStrategy = coalesceStrategy
		self.downstreamAPIs = downstreamAPIs


	def setCoalesceStrategy(self, coalesce_strategy):
		self.coalesceStrategy = coalesce_strategy


	def runDownstreamAPI(self, api, member_id, output_buffer, index):
		api_response = api.call(member_id)
		# We can define how we want to handle bad API response,
		# for simplicity, I will write failure
		if not self.verifyResponse(api_response):
			output_buffer[index] = 'FAILURE'
		else:
			output_buffer[index] = api_response


	def verifyResponse(self, response):
		keys = response.keys()
		return len(response) == 3 and 'deductible' in keys and 'stop_loss' in keys and 'oop_max' in keys


	def call(self, member_id):
		# allocate the output list
		downstream_responses = [[]] * len(self.downstreamAPIs)
		api_threads = []

		# APIs are usually asynchronous, we kick off different threads for each API
		for i, api in enumerate(self.downstreamAPIs):
			t = threading.Thread(target=self.runDownstreamAPI, args=(api, member_id, downstream_responses, i,))
			api_threads.append(t)
			t.start()

		# wait for the threads to finish
		for t in api_threads:
			t.join()

		if 'FAILURE' in downstream_responses:
			return 'FAILURE'

		return self.coalesceStrategy(downstream_responses)


