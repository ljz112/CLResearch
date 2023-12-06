import processOrigin

def parseOrigin(query, language):
    try: 
        queryOrigin = processOrigin.getAllRoots(query, language)
        return queryOrigin
    except Exception as e:
        print(f"Wasn't able to get origin: {e}")
        return []





if __name__ == "__main__":
    query = 'Trevor Noah'
    language = 'en'
    # print(parseOrigin(query, language))
