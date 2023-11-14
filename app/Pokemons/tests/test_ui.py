import random

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver import FirefoxOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class UITests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        cls.selenium = webdriver.Firefox(options=opts)
        cls.action = ActionChains(cls.selenium)
        cls.selenium.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.pokemons = ['bulbasaur', 'ivysaur', 'venusaur', 'charmander', 'charmeleon', 'charizard', 'squirtle',
                         'wartortle', 'blastoise', 'caterpie', 'metapod', 'butterfree', 'weedle', 'kakuna', 'beedrill',
                         'pidgey', 'pidgeotto', 'pidgeot', 'rattata', 'raticate', 'spearow', 'fearow', 'ekans', 'arbok',
                         'pikachu', 'raichu', 'sandshrew', 'sandslash', 'nidoran-f', 'nidorina', 'nidoqueen',
                         'nidoran-m', 'nidorino', 'nidoking', 'clefairy', 'clefable', 'vulpix', 'ninetales',
                         'jigglypuff', 'wigglytuff', 'zubat', 'golbat', 'oddish', 'gloom', 'vileplume', 'paras',
                         'parasect', 'venonat', 'venomoth', 'diglett', 'dugtrio', 'meowth', 'persian', 'psyduck',
                         'golduck', 'mankey', 'primeape', 'growlithe', 'arcanine', 'poliwag', 'poliwhirl', 'poliwrath',
                         'abra', 'kadabra', 'alakazam', 'machop', 'machoke', 'machamp', 'bellsprout', 'weepinbell',
                         'victreebel', 'tentacool', 'tentacruel', 'geodude', 'graveler', 'golem', 'ponyta', 'rapidash',
                         'slowpoke', 'slowbro', 'magnemite', 'magneton', 'farfetchd', 'doduo', 'dodrio', 'seel',
                         'dewgong', 'grimer', 'muk', 'shellder', 'cloyster', 'gastly', 'haunter', 'gengar', 'onix',
                         'drowzee', 'hypno', 'krabby', 'kingler', 'voltorb']
        self.bulbasaur = """Свойства
id 1
name bulbasaur
hp 45
attack 49
defense 49
base_experience 64
height 7
weight 69
species bulbasaur"""

    def test_index_page(self):
        self.selenium.get(f"{self.live_server_url}{reverse('Pokemons.index')}")
        elems = [elem.text for elem in self.selenium.find_elements(By.CLASS_NAME, 'card-title')]
        self.assertEqual(elems, self.pokemons)
        modal = self.selenium.find_element(By.ID, 'modal')
        self.assertFalse(modal.is_displayed())
        menu = self.selenium.find_element(By.ID, 'menu')
        self.assertFalse(menu.is_displayed())
        toast = self.selenium.find_element(By.ID, 'toast')
        self.assertFalse(toast.is_displayed())
        prev_page_button = self.selenium.find_element(By.ID, 'prev-page')
        self.assertEqual(prev_page_button.get_attribute('onclick'), "window.location.href = 'None'")
        next_page_button = self.selenium.find_element(By.ID, 'next-page')
        self.assertEqual(next_page_button.get_attribute('onclick'),
                         "window.location.href = '/pokemons/api/pokemon/list/?offset=100&limit=100'")

    def test_pokemon_properties(self):
        self.selenium.get(f"{self.live_server_url}{reverse('Pokemons.index')}")
        bulbasaur = self.selenium.find_element(By.XPATH, "//div[@id='grid']/div[1]")
        self.action.context_click(bulbasaur).perform()
        menu = self.selenium.find_element(By.ID, 'menu')
        self.assertTrue(menu.is_displayed())
        self.selenium.find_element(By.ID, 'properties-submit').click()
        WebDriverWait(self.selenium, 3).until(
            expected_conditions.visibility_of_element_located(
                (By.ID, 'modal'),
            )
        )
        modal = self.selenium.find_element(By.ID, 'modal')
        self.assertTrue(modal.is_displayed())
        self.assertEqual(modal.text, self.bulbasaur)

    def test_search(self):
        self.selenium.get(f"{self.live_server_url}{reverse('Pokemons.index')}")
        searchbar = self.selenium.find_element(By.ID, 'searchbar')
        inp = searchbar.find_element(By.NAME, "name")
        inp.send_keys('bulbasaur')
        self.selenium.find_element(By.XPATH, "//form[@id='searchbar']/button[1]").click()
        WebDriverWait(self.selenium, 3).until(
            expected_conditions.url_contains('?action=Search&name=bulbasaur')
        )
        self.assertEqual(self.selenium.find_elements(By.CLASS_NAME, 'card-title')[0].text, 'bulbasaur')
        self.selenium.back()
        WebDriverWait(self.selenium, 3).until(
            expected_conditions.url_to_be(f"{self.live_server_url}{reverse('Pokemons.index')}")
        )
        searchbar = self.selenium.find_element(By.ID, 'searchbar')
        inp = searchbar.find_element(By.NAME, "name")
        inp.clear()
        inp.send_keys('bulbasaurus')
        self.selenium.find_element(By.XPATH, "//form[@id='searchbar']/button[1]").click()
        WebDriverWait(self.selenium, 3).until(
            expected_conditions.url_contains('?action=Search&name=bulbasaurus')
        )
        self.assertEqual(self.selenium.find_element(By.ID, 'errors').text, 'not found')

    def test_battle(self):
        random.seed(42)
        self.selenium.get(f"{self.live_server_url}{reverse('Pokemons.index')}")
        bulbasaur = self.selenium.find_element(By.XPATH, "//div[@id='grid']/div[1]")
        self.action.context_click(bulbasaur).perform()
        menu = self.selenium.find_element(By.ID, 'menu')
        self.assertTrue(menu.is_displayed())
        self.selenium.find_element(By.ID, 'battle-submit').click()
        WebDriverWait(self.selenium, 3).until(
            expected_conditions.url_contains('battle/?playerPokemon=bulbasaur&opponentPokemon=houndoom')
        )
        self.assertEqual(self.selenium.find_element(By.ID, 'player_name').text, 'bulbasaur')
        self.assertEqual(self.selenium.find_element(By.ID, 'opponent_name').text, 'houndoom')
        hit_form = self.selenium.find_element(By.ID, 'hit-form')
        inp = hit_form.find_element(By.ID, 'hit-number')
        inp.clear()
        inp.send_keys(4)
        inp.submit()
        WebDriverWait(self.selenium, 3).until(
            expected_conditions.text_to_be_present_in_element((By.ID, 'battle-log'), 'бьет')
        )
        self.assertEqual(self.selenium.find_element(By.XPATH, "//div[@id='battle-log']/div[1]").text,
                         'houndoom бьет bulbasaur и наносит 47 урона')
