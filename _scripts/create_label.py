import os

def scantag(path):
    front_matter_started = False
    with open(path, 'r') as file:
        for line in file:
            if line.startswith('---'):
                if front_matter_started:
                    return set()
                else:
                    front_matter_started = True
            elif front_matter_started:
                if line.startswith('tags:'):
                    tags_str = line[len('tags:'):-1].strip(' []')
                    return set(token.strip() for token in tags_str.split(',') if token.strip())
    return set()

                

if __name__ == "__main__":
    paths = [os.path.join('_posts', file) for file in os.listdir('_posts')]
    paths = [path for path in paths if path.endswith('.md')]

    tags = set()
    for path in paths:
        tags = tags | scantag(path)
    
    for tag in tags:
        tag_path = os.path.join("tag", tag + ".html")
        if not os.path.exists(tag_path):
            with open(tag_path, 'w') as f:
                f.write("---\n")
                f.write("layout: default\n")
                f.write("title: Search by tag\n")
                f.write(f"tag: {tag}\n")
                f.write("---\n")
                f.write("{% include tag_page.html tag=page.tag %}\n")
