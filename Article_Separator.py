import os
# Specify the input file and output directory
input_file = r'cant sep/Rashtrasanchar/vishleshan_articles.txt'
output_dir = r'Rashtrasanchar/vishleshan'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the content of the input file
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Split the content by blank lines
articles = content.split('\n\n\n')
print("Number of articles: ", len(articles))

article_num=1
# Write each article to a separate text file
for i, article in enumerate(articles):
    # Generate a filename for each article
    article=article.strip()
    if article:
        output_file = os.path.join(output_dir, f'article_{article_num}.txt')
        article_num+=1
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(article)

print(f'Successfully separated {len(articles)} articles into individual files.')


# article_num=0
# for i in range(1,21000,1000):
#     # Specify the input file and output directory
#     input_file = f'Shardul\\Lokmat Maharashtra\\lokmat_maharashtra_page_{i}_to_{i+999}.txt'

#     # Read the content of the input file
#     with open(input_file, 'r', encoding='utf-8') as file:
#         content = file.read()

#     # Split the content by blank lines
#     articles = content.split('\n')
#     print("Number of articles: ", len(articles))

#     # Write each article to a separate text file
#     for i, article in enumerate(articles):
#         if article:
#             article_num+=1
#             # Generate a filename for each article
#             output_dir = f'Shardul Separated\\Lokmat Maharashtra\\page_{((article_num-1)//5000)*5000 + 1}_to_{((article_num-1)//5000)*5000 + 5000}'

#             # Create the output directory if it doesn't exist
#             if not os.path.exists(output_dir):
#                 os.makedirs(output_dir)

#             output_file = os.path.join(output_dir, f'article_{article_num}.txt')
#             with open(output_file, 'w', encoding='utf-8') as file:
#                 file.write(article)

#     print(f'Successfully separated {len(articles)} articles into individual files.')
