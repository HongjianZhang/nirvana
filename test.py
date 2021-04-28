from NirvanaAPI import NirvanaAPI, DownstreamAPI
import CoalesceStrategy 


API1 = DownstreamAPI({1: {"deductible": 1000, "stop_loss": 10000, "oop_max": 5000}, 2: {"deductible": 1000, "stop_loss": 10000}})
API2 = DownstreamAPI({1: {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000}, 2: {"deductible": 1200, "stop_loss": 13000, "oop_max": 6000}})
API3 = DownstreamAPI({1: {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000}, 2: {"deductible": 1000, "stop_loss": 10000, "oop_max": 6000}})


APIs = [API1, API2, API3]


def assertResponse(response, deductible, stop_loss, oop_max):
	assert len(response) == 3
	assert response["deductible"] == deductible
	assert response["stop_loss"] == stop_loss
	assert response["oop_max"] == oop_max


def testAverageCoalesceStrategy():
	nirvana_api = NirvanaAPI(CoalesceStrategy.averageCoalesceStrategy, APIs)
	response = nirvana_api.call(1)
	print(response)
	assertResponse(response, 1066, 11000, 5666)
	print('averageCoalesceStrategy succeeded')


def testMaxCoalesceStrategy():
	nirvana_api = NirvanaAPI(CoalesceStrategy.maxCoalesceStrategy, APIs)
	response = nirvana_api.call(1)
	assertResponse(response, 1200, 13000, 6000)
	print('maxCoalesceStrategy succeeded')


def testSwitchCoalesceStrategy():
	nirvana_api = NirvanaAPI(CoalesceStrategy.averageCoalesceStrategy, APIs)
	response = nirvana_api.call(1)
	assertResponse(response, 1066, 11000, 5666)

	nirvana_api.setCoalesceStrategy(CoalesceStrategy.maxCoalesceStrategy)
	response = nirvana_api.call(1)
	assertResponse(response, 1200, 13000, 6000)
	print('switch strategy succeeded')

def testInvalidAPIResponse():
	nirvana_api = NirvanaAPI(CoalesceStrategy.averageCoalesceStrategy, APIs)
	response = nirvana_api.call(2)
	assert response == 'FAILURE'
	print('invalid response test succeeded')


if __name__ == "__main__":
    testAverageCoalesceStrategy()
    testMaxCoalesceStrategy()
    testSwitchCoalesceStrategy()
    testInvalidAPIResponse()