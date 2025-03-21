def top_ten_artists_query(country) -> dict:
    views_field = f"views_per_country.{country}"
    query = {
        "bool": {
            "filter": [{"exists": {"field": views_field}}],
        }
    }
    aggs = {
        "top_ten_artists": {
            "terms": {
                "field": "artist",
                "size": 10,  # 前 10 名
                "order": {"views": "desc"},
            },
            "aggs": {
                "views": {
                    "sum": {
                        "field": views_field,
                        "missing": 0,
                    }
                }
            },
        }
    }
    return {"index": "songs_index", "query": query, "size": 0, "aggs": aggs}


def top_ten_songs_query(country) -> dict:
    views_field = f"views_per_country.{country}"
    query = {
        "bool": {
            "filter": [{"exists": {"field": views_field}}],
        }
    }
    sort = {views_field: {"order": "desc"}}
    source = [
        "title",
        views_field,
        "album.title",
        "artist",
    ]
    return {
        "index": "songs_index",
        "query": query,
        "size": 10,
        "sort": sort,
        "source": source,
    }
