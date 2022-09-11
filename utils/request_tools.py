def build_query_params(query_params_list: list[tuple]) -> dict:
    result = {}

    for query_param in query_params_list:
        result[query_param[0]] = query_param[1]

    return result
