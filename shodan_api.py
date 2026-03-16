import shodan


class ShodanClient:

    def __init__(self, api_key):

        self.api = shodan.Shodan(api_key)

    def search(self, query, limit=20):

        results = self.api.search(query)

        data = []

        for r in results["matches"][:limit]:

            row = {

                "ip": r.get("ip_str"),
                "port": r.get("port"),
                "org": r.get("org"),
                "isp": r.get("isp"),
                "asn": r.get("asn"),
                "country": r.get("location", {}).get("country_name"),
                "city": r.get("location", {}).get("city"),
                "hostnames": ",".join(r.get("hostnames", [])),
                "domains": ",".join(r.get("domains", [])),
                "product": r.get("product"),
                "version": r.get("version")
            }

            data.append(row)

        return data
