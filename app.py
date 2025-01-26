import requests
import argparse


class DataAnalysis:
    def __init__(self, dataSourceName, analysisFlowId=None):
        """
        Initialize the DataAnalysis class with the data source name and analysis flow id.
        Raises an exception if the input is not supported.
        """
        self._text_to_func = {
            "Stackoverflow": self._extract_stackoverflow_commits,
            "Github": self._extract_github_messages
        }
        self._text_to_api = {
            "Stackoverflow": "https://api.stackexchange.com/2.2/tags/highcharts/faq?site=stackoverflow",
            "Github": "https://api.github.com/repos/highcharts/highcharts/commits"
        }
        self._analysisFlow = {
            "1": [
                {
                    "Name": "Remove short items",
                    "func": self._remove_short_items
                },
                {
                    "Name": "Remove spaces",
                    "func": self._remove_spaces
                }
            ]
        }
        if dataSourceName not in self._text_to_func:
            raise Exception("Unsupported data source")
        if analysisFlowId and analysisFlowId not in self._analysisFlow:
            raise Exception("Invalid analysis flow")
        self._dataSourceName = dataSourceName
        self._analysisFlowId = analysisFlowId

    def _fetch_data(self):
        """
            Fetch data from the data source
        """
        try:
            response = requests.get(self._text_to_api[self._dataSourceName])
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return f"An error occurred: {str(e)}"

    def _extract_stackoverflow_commits(self, data):
        """
        Extracts the title of the items from the stackoverflow data, 
        skipping items without titles
        """
        items = data.get("items", [])
        return [item["title"] for item in items if "title" in item]

    def _extract_github_messages(self, data):
        """
        Extracts the commit messages from the github data,
        skipping commits without messages
        """
        return [commit["commit"]["message"]
                for commit in data
                if "commit" in commit and "message" in commit["commit"]]

    def _remove_short_items(self, data):
        """
            Remove items with length less than 5    
        """
        return [item for item in data if len(item) > 5]

    def _remove_spaces(self, data):
        """
            Remove spaces from the items
        """
        return [item.replace(" ", "") for item in data]

    def _apply_analysis_flow(self, data):
        """
            Apply the analysis flow to the data
        """
        for step in self._analysisFlow[self._analysisFlowId]:
            data = step["func"](data)
        return data

    def analyze(self):
        """
            This function fetches the data from the data source 
            and applies the analysis flow to the data
        """
        try:
            data = self._fetch_data()
            if isinstance(data, str):
                return [data]
            extracted_data = self._text_to_func[self._dataSourceName](data)
            if self._analysisFlowId:
                extracted_data = self._apply_analysis_flow(extracted_data)
            return extracted_data
        except Exception as e:
            return [str(e)]


def Analyze(dataSourceName, analysisFlowId=None):
    try:
        dataAnalysis = DataAnalysis(dataSourceName, analysisFlowId)
        return dataAnalysis.analyze()
    except Exception as e:
        return [str(e)]


def main():
    parser = argparse.ArgumentParser(description='Analyze data')
    parser.add_argument('dataSourceName', type=str, help='Data source name')
    parser.add_argument('analysisFlowId', type=str,
                        nargs='?', help='Analysis flow id')
    args = parser.parse_args()
    dataSourceName = args.dataSourceName
    analysisFlowId = args.analysisFlowId
    print(Analyze(dataSourceName, analysisFlowId))


if __name__ == '__main__':
    main()
