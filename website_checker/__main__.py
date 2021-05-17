import fire
import website_checker


def produce():
    website_checker.producer.main()


def consume():
    website_checker.consumer.main()


fire.Fire()
