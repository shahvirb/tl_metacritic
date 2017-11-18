#import tl_saved
import tl_fetch
import tl_parse
import meta_scraper
import jinja2
from jinja2 import Environment, FileSystemLoader
import os
import threading
import metered
from contextlib import contextmanager
import time
import import_hack as ih
import logging
import pprint
import click


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass

def gen_report_html(template, vars):
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(template))),
                         autoescape=True, trim_blocks=True)
    return j2_env.get_template(os.path.basename(template)).render(vars)
    
def write_html(outfile, html):
    with open(outfile, 'w') as f:
        f.write(html)

def process_torrent(title, lock, game_data):
    logger.info("Searching: " + title['title'])
    data = {}
    data["torrent_title"] = title['title']
    results = meta_scraper.brute_search(title['title'])
    if results:
        best = results[0]
        if best['url']:
            data['title'] = best['title']
            logger.info("Found: " + best['title'])
            logger.info(best['url'])
            review = meta_scraper.get_review_data(best['url'])
            if review:
                data.update(review)
            data['tlurl'] = title['url']
            logger.info(pprint.pformat(data))
    with lock:
        game_data.append(data)

class LimitedThread(threading.Thread):
    def __init__(self, worker, max_semaphore, *args):
        self.max_semaphore = max_semaphore
        self.worker = worker
        self.args = args
        super(LimitedThread, self).__init__()

    def run(self):
        with self.max_semaphore:
            self.worker(*self.args)

def audit_game_data(game_data):
    review_title_count = 0
    title_count = 0
    for gd in game_data:
        with ignored(KeyError): review_title_count += 1 if gd['title'] else 0
        with ignored(KeyError): title_count += 1 if gd['torrent_title'] else 0
    logger.info('AUDIT >> len(game_data): {}, title_count: {}, review_title_count: {}'.format(len(game_data), title_count, review_title_count))


@click.command()
@click.argument('outfile', type=click.Path(exists=False))
@click.option('--pages', '-p', type=int, default=1, help='Number of TL pages to scrape')
@click.option('--max', '-m', type=int, default=0, help='Max number of results. 0 == No limit')
@click.option('-mt', '--max_threads', type=int, default=4, help='Max number of threads')
def main(outfile, pages, max, max_threads=4):
    session = tl_fetch.Session()
    game_data = []
    threads = []
    data_lock = threading.Lock()
    max_semaphore = threading.BoundedSemaphore(max_threads)
    meter = metered.Meter(0.002)
    
    # -------------- TL SCRAPE 
    for page in range(pages):
        page += 1
        html = tl_fetch.get_pc_games_page(session, page)
        #soup = tl_saved.get_soup("saved.html")
        soup = tl_parse.make_html_soup(html)
        titles = tl_parse.parse_torrent_titles(soup)
    
        results = 0
        for i, title in enumerate(titles):
            meter.run(process_torrent, title, data_lock, game_data)
            results += 1
            if max and results >= max:
                break
    # --------------
    
    # -------------- IMPORT HACK
    # for title in ih.get_titles():
    #         meter.run(process_torrent, title, data_lock, game_data)
    # --------------

    #for t in threads: t.start()
    #for t in threads: t.join()
    meter.set_prev_now()
    while not meter.timed_out(4): meter.work()
    
    audit_game_data(game_data)
    vars = {"game_data": game_data}
    html = gen_report_html('web/template.html', vars)
    write_html(outfile, html)
    logger.info("Report Written: {}".format(outfile))
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    main()