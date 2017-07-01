
#add by me

    def infoh(self,*arg):
        """ Print chunk information of victim"""
        (victim,) = normalize_argv(arg,1)
        angelheap.infoh(victim)

    def getinfoh(self,*arg):
        """ Print chunk information of victim"""
        (victim,) = normalize_argv(arg,1)
        angelheap.getinfoh(victim)

    def parseh(self):
        """ Print chunk information of victim"""
        #(victim,) = normalize_argv(arg,1)
        angelheap.parseh()

    def getheaplist(self, *arg):
        """ Print chunk information of victim"""
        (lst,) = normalize_argv(arg,1)
        angelheap.getheaplist(lst)

    def ci(self,*arg):
        """ Print chunk information of victim"""
        (victim,) = normalize_argv(arg,1)
        angelheap.ci(victim)

    def allci(self):
        """ Print chunk information of victim"""
        angelheap.allci()

#added by me

