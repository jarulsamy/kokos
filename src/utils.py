def JoinDict(*dicts):
	joined = {}
	for dict in dicts:
		for key, value in dict.items():
			joined[key] = value
	return joined
