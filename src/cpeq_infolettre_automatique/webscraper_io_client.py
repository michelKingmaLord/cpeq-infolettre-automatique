import httpx


class WebscraperIoClient:
    def get_endpoint(self, url: str) -> dict:
        response = httpx.get(url)
        return self._handle_response(response)

    def _handle_response(self, response):
        pass
