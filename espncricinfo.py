import scrapy
import re

class EspncricinfoSpider(scrapy.Spider):
    name = "espncricinfo"
    allowed_domains = ["espncricinfo.com"]
    start_urls = ["https://www.espncricinfo.com/records/tournament/team-match-results/indian-premier-league-2023-15129"]
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    match_id = 1

    def __init__(self, *args, **kwargs):
        super(EspncricinfoSpider, self).__init__(*args, **kwargs)
        self.match_id_counter = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.header)

    def parse(self, response):
        boards = response.xpath("//div[@class='ds-p-0']/div/div[@class='ds-overflow-x-auto ds-scrollbar-hide']")
        for rows in boards:
            row = rows.xpath(".//table/tbody/tr")
            for team in row:
                fteam = team.xpath(".//td[@class='ds-min-w-max']/span/a/span/text()").get()
                steam = team.xpath(".//td[@class='ds-min-w-max ds-text-right']/span/a[@class='ds-inline-flex ds-items-start ds-leading-none']/span/text()").get()
                winner = team.xpath("(.//td[@class='ds-min-w-max ds-text-right'])[2]/span/text()").get()
                margin = team.xpath("(.//td[@class='ds-min-w-max ds-text-right'])[3]/span/text()").get()
                ground = team.xpath("(.//td[@class='ds-min-w-max ds-text-right'])[4]/span/a[@class='ds-inline-flex ds-items-start ds-leading-none']/span/text()").get()
                date = team.xpath(".//td[@class='ds-min-w-max ds-text-right ds-whitespace-nowrap']/span/text()").get()
                scoreboard = team.xpath(".//td[@class='ds-min-w-max ds-text-right']/span/a[@title='Twenty20']/@href").get()
                sblink = "https://www.espncricinfo.com"+scoreboard if scoreboard else None
                
                # yield{
                #     "Match_Id":self.match_id,
                #     "Team 1": fteam,
                #     "Team 2": steam,
                #     "Team": fteam +" Vs "+ steam,
                #     "Winner": winner,
                #     "Margin": margin,
                #     "Ground": ground,
                #     "Date": date,
                #     "Scoreboard Link": sblink
                # }
                matchid_list = []
                self.match_id += 1
                matchid_list.append(self.match_id) 
                self.match_id_counter += 1
                yield scrapy.Request(url=sblink, callback=self.parse_sb, headers=self.header, cb_kwargs={'matchs_id': self.match_id_counter})
    
    def parse_sb(self,response,matchs_id):
        scores = response.xpath("//div[@class='ds-grow']/div[@class='ds-mt-3']/div")
                            
        for card in scores:
            team1 = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2']/div/div/div[@class='ds-flex ds-flex-col ds-grow ds-justify-center']/span/span/text()").get()
            team2 = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div/div/span/span/text()").get()
            # team = team1 + " Vs " + team2
            playername1 = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-flex ds-items-center'] | .//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-flex ds-items-center ds-border-line-primary ci-scorecard-player-notout']")
            team_list1 = []
            out_list1 = []  
            run_list1 = []             
            ball_list1 = []  
            four_list1 = []
            six_list1 = []
            strike_list1 = []  

            for index, players in enumerate(playername1, start=1):
                teamn = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div/div")
                for team in teamn:
                    teams = team.xpath(".//span/span/text()").get()
                    team_list1.append(teams)
                playerpos = index
                player = players.xpath(".//a[@class='ds-inline-flex ds-items-start ds-leading-none']/span/span/text()").get()                                                                         
                bowler = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-min-w-max !ds-pl-[100px]']")
                for bname in bowler:
                    out = bname.xpath(".//span/span/text()").get()
                    out_list1.append(out)
                runs = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-typo']")
                for r in runs:
                    run = r.xpath(".//strong/text()").get()
                    run_list1.append(run)
                balls = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][1]")
                for b in balls:
                    ball = b.xpath(".//text()").get()
                    ball_list1.append(ball)
                fours  = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][2]")
                for f in fours:
                    four = f.xpath(".//text()").get()
                    four_list1.append(four)
                sixs = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][3]")
                for s in sixs:
                    six = s.xpath(".//text()").get()
                    six_list1.append(six)
                strikerates = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][4]")
                for sr in strikerates:
                    strike = sr.xpath(".//text()").get()
                    strike_list1.append(strike)
                # yield{
                #     # "Team 1":team1,
                #     # "Team 2":team2,
                #     "Match_Id":matchs_id,
                #     "Team": team1 + ' Vs ' + team2,
                #     "Batting Team":team_list1[index-1],
                #     "Player Name":player,
                #     "Player Position":playerpos,
                #     "Out":out_list1[index-1],
                #     "Run":run_list1[index-1],
                #     "Ball":ball_list1[index-1],
                #     "Four":four_list1[index-1],
                #     "Six":six_list1[index-1],
                #     "StrikeRate":strike_list1[index-1]
                # }

            for players in playername1:
                teamn = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div/div")
                player = players.xpath(".//a/span/span/text()").get()                                                                         
                playerl = players.xpath(".//a/@href").get() 
                plink = "https://www.espncricinfo.com"+playerl  

                # yield{
                #     "Player Name":player,
                #     "Player Link":plink
                # }  
                yield scrapy.Request(url=plink, callback=self.parse_player, headers=self.header)

                
            

            playername2 = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-flex ds-items-center'] | .//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-flex ds-items-center ds-border-line-primary ci-scorecard-player-notout']")
            team_list2 = []
            out_list2 = []
            run_list2 = []
            ball_list2 = []
            four_list2 = []
            six_list2 = []
            strike_list2 = []
            
            for index, players in enumerate(playername2, start=1):
                teamn = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div/div")
                for team in teamn:
                    teams = team.xpath(".//span/span/text()").get()
                    team_list2.append(teams)
                playerpos = index
                player = players.xpath(".//a[@class='ds-inline-flex ds-items-start ds-leading-none']/span/span/text()").get()                                                                         
                bowler = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-min-w-max !ds-pl-[100px]']")
                for bname in bowler:
                    out = bname.xpath(".//span/span/text()").get()
                    out_list2.append(out)
                runs = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right ds-text-typo']")
                for r in runs:
                    run = r.xpath(".//strong/text()").get()
                    run_list2.append(run)
                balls = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][1]")
                for b in balls:
                    ball = b.xpath(".//text()").get()
                    ball_list2.append(ball)
                fours  = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][2]")
                for f in fours:
                    four = f.xpath(".//text()").get()
                    four_list2.append(four)
                sixs = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][3]")
                for s in sixs:
                    six = s.xpath(".//text()").get()
                    six_list2.append(six)
                strikerates = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][4]")
                for sr in strikerates:
                    strike = sr.xpath(".//text()").get()
                    strike_list2.append(strike)
                # yield{
                #     # "Team 1":team1,
                #     # "Team 2":team2,
                #     "Match_Id":matchs_id,
                #     "Team": team1 + ' Vs ' + team2,
                #     "Batting Team":team_list2[index-1],
                #     "Player Name":player,
                #     "Player Position":playerpos,
                #     "Out":out_list2[index-1],
                #     "Run":run_list2[index-1],
                #     "Ball":ball_list2[index-1],
                #     "Four":four_list2[index-1],
                #     "Six":six_list2[index-1],
                #     "StrikeRate":strike_list2[index-1]
                # }

            for players in playername1:
                teamn = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div/div")
                player = players.xpath(".//a[@class='ds-inline-flex ds-items-start ds-leading-none']/span/span/text()").get()                                                                       
                playerl = players.xpath(".//a[@class='ds-inline-flex ds-items-start ds-leading-none']/@href").get() 
                plink = "https://www.espncricinfo.com"+playerl                                                                      
                
            # yield{
            #         "Player Name":player,
            #         "Player Link":plink
            #     }     
            yield scrapy.Request(url=plink, callback=self.parse_player, headers=self.header)


            bowlername1 = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-flex ds-items-center']")
            bteam_list1 = []
            over_list1 = []
            maiden_list1 = []
            orun_list1 = []
            wicket_list1 = []
            eco_list1 = []
            zero_list1 = []
            wide_list1 = []
            noball_list1 = []
            for index, bowlers in enumerate(bowlername1, start=1):
                teamn = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div/div")
                for team in teamn:
                    teams = team.xpath(".//span/span/text()").get()
                    bteam_list1.append(teams)
                bowler = bowlers.xpath(".//a/span/text()").get()
                # overs= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][1]")
                overs= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][1 ]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][1]")
                for o in overs:
                    over = o.xpath(".//text()").get()
                    over_list1.append(over)
                # maidens= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][2]")
                maidens= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][2]")
                for m in maidens:
                    maiden = m.xpath(".//text()").get()
                    maiden_list1.append(maiden)
                # oruns= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][3]")
                oruns= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][3]")
                for ors in oruns:
                    orun = ors.xpath(".//text()").get()
                    orun_list1.append(orun)
                wickets= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-text-right']")
                for w in wickets:
                    wicket = w.xpath(".//span/strong/text()").get()
                    wicket_list1.append(wicket)
                # economies= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][4]")
                economies= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][4]")
                for ec in economies:
                    economy = ec.xpath(".//text()").get()
                    eco_list1.append(economy)
                # zeros= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][5]")
                zeros= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][5]")
                for zs in zeros:
                    zero = zs.xpath(".//text()").get()
                    zero_list1.append(zero)
                wides = response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][8]")
                for ws in wides:
                    wide = ws.xpath(".//text()").get()
                    wide_list1.append(wide)
                # noballs= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][6]")
                noballs= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][9]")
                for nb in noballs:
                    noball = nb.xpath(".//text()").get()
                    noball_list1.append(noball)
                
                # yield{
                #     "Match_Id":matchs_id,
                #     "Team": team1 + ' Vs ' + team2,
                #     "Bowling Team":bteam_list1[index-1],
                #     "Bowler Name":bowler,
                #     "Overs":over_list1[index-1],
                #     "Maidens":maiden_list1[index-1],
                #     "Runs":orun_list1[index-1],
                #     "Wickets":wicket_list1[index-1],
                #     "Economy":eco_list1[index-1],
                #     "Zeros":zero_list1[index-1],
                #     "Wides":wide_list1[index-1],
                #     "No Ball":noball_list1[index-1]
                # }
            
            for bowlers in bowlername1:
                teamn = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2 ]/div/div/div")
                bowler = bowlers.xpath(".//a/span/text()").get()                                                                       
                bowlerl = bowlers.xpath(".//a/@href").get()                                                                       
                plink = "https://www.espncricinfo.com"+bowlerl                                                                     
                
            # yield{
            #         "Player Name":player,
            #         "Player Link":plink
            #     }     
            yield scrapy.Request(url=plink, callback=self.parse_player, headers=self.header)


            bowlername2 = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-flex ds-items-center']")
            bteam_list2 = []
            over_list2 = []
            maiden_list2 = []
            orun_list2 = []
            wicket_list2 = []
            eco_list2 = []
            zero_list2 = []
            wide_list2 = []
            noball_list2 = []
            for index, bowlers in enumerate(bowlername2, start=1):
                teamn = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div/div")
                for team in teamn:
                    teams = team.xpath(".//span/span/text()").get()
                    bteam_list2.append(teams)
                bowler = bowlers.xpath(".//a/span/text()").get()
                # overs= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][2]")
                overs= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][1]")
                for o in overs:
                    over = o.xpath(".//text()").get()
                    over_list2.append(over)
                # maidens= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][2]")
                maidens= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][2]")
                for m in maidens:
                    maiden = m.xpath(".//text()").get()
                    maiden_list2.append(maiden)
                # oruns= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][3]")
                oruns= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][3]")
                for ors in oruns:
                    orun = ors.xpath(".//text()").get()
                    orun_list2.append(orun)
                wickets= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-text-right']")
                for w in wickets:
                    wicket = w.xpath(".//span/strong/text()").get()
                    wicket_list2.append(wicket)
                # economies= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][4]")
                economies= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][4]")
                for ec in economies:
                    economy = ec.xpath(".//text()").get()
                    eco_list2.append(economy)
                zeros= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][5]")
                for zs in zeros:
                    zero = zs.xpath(".//text()").get()
                    zero_list2.append(zero)
                # wides= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][5]")
                wides = response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][8]")
                for ws in wides:
                    wide = ws.xpath(".//text()").get()
                    wide_list2.append(wide)
                # noballs= card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][6]")
                noballs= response.xpath("//div[@class='ds-rounded-lg ds-mt-2'][2]/div/div[@class='ds-p-0']/table[@class='ds-w-full ds-table ds-table-md ds-table-auto ']/tbody/tr/td[@class='ds-w-0 ds-whitespace-nowrap ds-min-w-max ds-text-right'][9]")
                for nb in noballs:
                    noball = nb.xpath(".//text()").get()
                    noball_list2.append(noball)

                # yield{
                #     "Match_Id":matchs_id,
                #     "Team": team1 + ' Vs ' + team2,
                #     "Bowling Team":bteam_list2[index-1],
                #     "Bowler Name":bowler,
                #     "Overs":over_list2[index-1],
                #     "Maidens":maiden_list2[index-1],
                #     "Runs":orun_list2[index-1],
                #     "Wickets":wicket_list2[index-1],
                #     "Economy":eco_list2[index-1],
                #     "Zeros":zero_list2[index-1],
                #     "Wides":wide_list2[index-1],
                #     "No Ball":noball_list2[index-1]
                # }
            
            for bowlers in bowlername2:
                teamn = card.xpath(".//div[@class='ds-rounded-lg ds-mt-2'][1]/div/div/div")
                bowler = bowlers.xpath(".//a/span/text()").get()                                                                       
                bowlerl = bowlers.xpath(".//a/@href").get()                                                                       
                plink = "https://www.espncricinfo.com"+bowlerl                                                                     
                
            # yield{
            #         "Player Name":player,
            #         "Player Link":plink
            #     }     
            
            yield scrapy.Request(url=plink, callback=self.parse_player, headers=self.header)

    def parse_player(self, response):
        playein = response.xpath("//div[@class='ds-p-4']/div")  
        link_list = []

        for index, players in enumerate(playein, start=1):
            playern = players.xpath("(.//div[1]/div/span/p/text())[1]").get()
            batst = players.xpath("(.//div[1]/div/span/p/text())[4]").get()
            ballst = players.xpath("(.//div[1]/div/span/p/text())[5]").get()
            role = players.xpath("(.//div[1]/div/span/p/text())[7]").get()
        
            yield{
                "Player Name":playern,
                "Batting Style":batst,
                "Bowling Style":ballst,
                # "Role":role,
                # "Image Link":link_list[index-1]
            }
            imgs = response.xpath("//div[@class='ds-relative ds-z-0']/div/div[2]/img/@src").get()
            for img in imgs:
                img
                yield{
                    "Image":img
                }
