import csv
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go


def get_colors(path):
    with open(path) as csvfile:
        df = pd.read_csv(csvfile)
        df = df.pivot_table(index=['performer'],
                            columns=['category'], values='l2').fillna(0)

        df.to_csv('grouped_data.csv')
    return df


def get_aster(path):
    with open(path) as csvfile:
        new_df = pd.read_csv(csvfile)
        new_df = new_df.pivot_table(index=['performer'],
                                    columns=['category'], values=['best_string'],
                                    aggfunc=lambda x: ''.join(str(v) for v in x)).fillna("")

        new_df.to_csv('new_grouped_data.csv')


def create_heatmap(df):
        data = []
        x_values = []
        y_values = []
        text = []
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

        with open('new_grouped_data.csv') as newlines:
            reader = csv.reader(newlines)
            for line in reader:
                if 'best_string' in line:
                    continue
                if 'performer' in line:
                    continue
                if 'category' in line:
                    continue
                else:
                    item = line[1:]
                    text.append(item)

        fig = ff.create_annotated_heatmap(z=data, x=x_values, y=y_values, annotation_text=text)
        fig.update_xaxes(side="bottom")
        fig.update_layout(xaxis=dict(title='Category'), yaxis=dict(title='Performer'))
        fig.show()
        fig.write_image("heatmap.pdf")


if __name__ == '__main__':
    get_colors('small_df.csv')
    get_aster('sumdf.csv')
    create_heatmap(get_colors('small_df.csv'))
