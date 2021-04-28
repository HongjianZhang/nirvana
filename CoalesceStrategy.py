# The coalesce strategies. Since each strategy is quite simple, we can simply represent them as functions


def averageCoalesceStrategy(data):
	deductibles = [response['deductible'] for response in data]
	stop_losses = [response['stop_loss'] for response in data]
	oop_maxes = [response['oop_max'] for response in data]

	return {"deductible": sum(deductibles)/len(deductibles), 
		"stop_loss": sum(stop_losses)/len(stop_losses),
		"oop_max": sum(oop_maxes)/len(oop_maxes)}


def maxCoalesceStrategy(data):
	deductibles = [response['deductible'] for response in data]
	stop_losses = [response['stop_loss'] for response in data]
	oop_maxes = [response['oop_max'] for response in data]

	return {"deductible": max(deductibles), 
		"stop_loss": max(stop_losses),
		"oop_max": max(oop_maxes)}