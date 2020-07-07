
import csv
import pandas as pd
import plotly.express as px


def create_heatmap(path):

    with open(path) as csvfile:
        data = []
        x_values = []
        y_values = []
        df = pd.read_csv(csvfile)
        df = df.pivot_table(index=['performer'],
                            columns=['category'], values='l2').fillna(0)

        df.to_csv('grouped_data.csv')

        with open('grouped_data.csv') as csvlines:
            reader = csv.reader(csvlines)
            for line in reader:
                if 'performer' in line:
                    continue
                else:
                    y_values.append(line[0])
                    item = line[1:]
                    data.append(item)
            for column in df.columns:
                x_values.append(column)

        fig = px.imshow(data,
                        labels=dict(x="Category", y="Performer", color="l2 value"),
                        x=x_values,
                        y=y_values
                       )
        fig.update_xaxes(side="bottom")
        fig.show()


if __name__ == '__main__':
    create_heatmap('small_df.csv')
